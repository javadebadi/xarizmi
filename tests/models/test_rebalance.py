import datetime

import pytest

from xarizmi.models.portfolio import Portfolio, PortfolioItem
from xarizmi.models.rebalance import (
    PortfolioAllocation,
    PortfolioAllocationItem,
    RebalanceResult,
    rebalance,
)
from xarizmi.models.symbol import Symbol


@pytest.fixture(scope="module")
def btc_symbol() -> Symbol:
    return Symbol.build(
        base_currency="BTC",
        quote_currency="USD",
        fee_currency="USD",
        exchange="BINANCE",
    )


@pytest.fixture(scope="module")
def eth_symbol() -> Symbol:
    return Symbol.build(
        base_currency="ETH",
        quote_currency="USD",
        fee_currency="USD",
        exchange="BINANCE",
    )


@pytest.fixture(scope="module")
def sol_symbol() -> Symbol:
    return Symbol.build(
        base_currency="SOL",
        quote_currency="USD",
        fee_currency="USD",
        exchange="BINANCE",
    )


@pytest.fixture
def portfolio(btc_symbol: Symbol, eth_symbol: Symbol) -> Portfolio:
    """BTC=80k, ETH=20k → total=100k, weights: 80%/20%."""
    return Portfolio(
        items=[
            PortfolioItem(
                symbol=btc_symbol,
                market_value=80_000,
                quantity=1,
                datetime=datetime.datetime(2024, 11, 26),
            ),
            PortfolioItem(
                symbol=eth_symbol,
                market_value=20_000,
                quantity=6,
                datetime=datetime.datetime(2024, 11, 26),
            ),
        ]
    )


class TestPortfolioAllocation:
    def test_valid_allocation(
        self, btc_symbol: Symbol, eth_symbol: Symbol
    ) -> None:
        alloc = PortfolioAllocation(
            items=[
                PortfolioAllocationItem(symbol=btc_symbol, weight=0.5),
                PortfolioAllocationItem(symbol=eth_symbol, weight=0.5),
            ]
        )
        assert len(alloc.items) == 2

    def test_weights_must_sum_to_one(
        self, btc_symbol: Symbol, eth_symbol: Symbol
    ) -> None:
        with pytest.raises(ValueError, match="sum to 1.0"):
            PortfolioAllocation(
                items=[
                    PortfolioAllocationItem(symbol=btc_symbol, weight=0.6),
                    PortfolioAllocationItem(symbol=eth_symbol, weight=0.6),
                ]
            )

    def test_negative_weight_raises(self, btc_symbol: Symbol) -> None:
        with pytest.raises(ValueError, match=">= 0"):
            PortfolioAllocationItem(symbol=btc_symbol, weight=-0.1)

    def test_empty_allocation_raises(self) -> None:
        with pytest.raises(ValueError, match="cannot be empty"):
            PortfolioAllocation(items=[])

    def test_getitem_found(
        self, btc_symbol: Symbol, eth_symbol: Symbol
    ) -> None:
        alloc = PortfolioAllocation(
            items=[
                PortfolioAllocationItem(symbol=btc_symbol, weight=0.7),
                PortfolioAllocationItem(symbol=eth_symbol, weight=0.3),
            ]
        )
        assert alloc[btc_symbol] == 0.7
        assert alloc[eth_symbol] == 0.3

    def test_getitem_not_found_returns_zero(
        self, btc_symbol: Symbol, eth_symbol: Symbol, sol_symbol: Symbol
    ) -> None:
        alloc = PortfolioAllocation(
            items=[
                PortfolioAllocationItem(symbol=btc_symbol, weight=0.6),
                PortfolioAllocationItem(symbol=eth_symbol, weight=0.4),
            ]
        )
        assert alloc[sol_symbol] == 0.0


class TestRebalance:
    def test_total_value(
        self,
        portfolio: Portfolio,
        btc_symbol: Symbol,
        eth_symbol: Symbol,
    ) -> None:
        target = PortfolioAllocation(
            items=[
                PortfolioAllocationItem(symbol=btc_symbol, weight=0.5),
                PortfolioAllocationItem(symbol=eth_symbol, weight=0.5),
            ]
        )
        result = rebalance(portfolio, target)
        assert result.total_value == 100_000

    def test_equal_split_from_skewed_portfolio(
        self,
        portfolio: Portfolio,
        btc_symbol: Symbol,
        eth_symbol: Symbol,
    ) -> None:
        # Portfolio: BTC=80k (80%), ETH=20k (20%)
        # Target: 50/50
        target = PortfolioAllocation(
            items=[
                PortfolioAllocationItem(symbol=btc_symbol, weight=0.5),
                PortfolioAllocationItem(symbol=eth_symbol, weight=0.5),
            ]
        )
        result = rebalance(portfolio, target)

        # BTC is overweight → sell 30k
        assert result[btc_symbol].delta_market_value == pytest.approx(-30_000)
        assert result[btc_symbol].current_weight == pytest.approx(0.8)
        assert result[btc_symbol].target_weight == pytest.approx(0.5)

        # ETH is underweight → buy 30k
        assert result[eth_symbol].delta_market_value == pytest.approx(30_000)
        assert result[eth_symbol].current_weight == pytest.approx(0.2)
        assert result[eth_symbol].target_weight == pytest.approx(0.5)

    def test_to_sell(
        self,
        portfolio: Portfolio,
        btc_symbol: Symbol,
        eth_symbol: Symbol,
    ) -> None:
        target = PortfolioAllocation(
            items=[
                PortfolioAllocationItem(symbol=btc_symbol, weight=0.5),
                PortfolioAllocationItem(symbol=eth_symbol, weight=0.5),
            ]
        )
        result = rebalance(portfolio, target)
        to_sell = result.to_sell()
        assert len(to_sell) == 1
        assert to_sell[0].symbol == btc_symbol
        assert to_sell[0].delta_market_value < 0

    def test_to_buy(
        self,
        portfolio: Portfolio,
        btc_symbol: Symbol,
        eth_symbol: Symbol,
    ) -> None:
        target = PortfolioAllocation(
            items=[
                PortfolioAllocationItem(symbol=btc_symbol, weight=0.5),
                PortfolioAllocationItem(symbol=eth_symbol, weight=0.5),
            ]
        )
        result = rebalance(portfolio, target)
        to_buy = result.to_buy()
        assert len(to_buy) == 1
        assert to_buy[0].symbol == eth_symbol
        assert to_buy[0].delta_market_value > 0

    def test_already_balanced_has_zero_deltas(
        self,
        portfolio: Portfolio,
        btc_symbol: Symbol,
        eth_symbol: Symbol,
    ) -> None:
        # Portfolio: BTC=80k (80%), ETH=20k (20%)
        # Target: same weights
        target = PortfolioAllocation(
            items=[
                PortfolioAllocationItem(symbol=btc_symbol, weight=0.8),
                PortfolioAllocationItem(symbol=eth_symbol, weight=0.2),
            ]
        )
        result = rebalance(portfolio, target)
        assert result.to_buy() == []
        assert result.to_sell() == []

    def test_new_symbol_in_target_not_in_portfolio(
        self,
        portfolio: Portfolio,
        btc_symbol: Symbol,
        eth_symbol: Symbol,
        sol_symbol: Symbol,
    ) -> None:
        # Add SOL with 10% weight, reduce others
        target = PortfolioAllocation(
            items=[
                PortfolioAllocationItem(symbol=btc_symbol, weight=0.5),
                PortfolioAllocationItem(symbol=eth_symbol, weight=0.4),
                PortfolioAllocationItem(symbol=sol_symbol, weight=0.1),
            ]
        )
        result = rebalance(portfolio, target)
        # SOL is not in portfolio → target_mv = 10k, delta = +10k
        assert result[sol_symbol].current_market_value == 0.0
        assert result[sol_symbol].target_market_value == pytest.approx(10_000)
        assert result[sol_symbol].delta_market_value == pytest.approx(10_000)
        assert sol_symbol in [i.symbol for i in result.to_buy()]

    def test_symbol_in_portfolio_not_in_target_gets_fully_sold(
        self,
        portfolio: Portfolio,
        btc_symbol: Symbol,
        eth_symbol: Symbol,
    ) -> None:
        # Target only has ETH → BTC should be fully sold
        target = PortfolioAllocation(
            items=[
                PortfolioAllocationItem(symbol=eth_symbol, weight=1.0),
            ]
        )
        result = rebalance(portfolio, target)
        assert result[btc_symbol].target_weight == 0.0
        assert result[btc_symbol].target_market_value == 0.0
        assert result[btc_symbol].delta_market_value == pytest.approx(-80_000)
        assert btc_symbol in [i.symbol for i in result.to_sell()]

    def test_getitem_not_found_returns_zero_item(
        self,
        portfolio: Portfolio,
        btc_symbol: Symbol,
        eth_symbol: Symbol,
        sol_symbol: Symbol,
    ) -> None:
        target = PortfolioAllocation(
            items=[
                PortfolioAllocationItem(symbol=btc_symbol, weight=0.5),
                PortfolioAllocationItem(symbol=eth_symbol, weight=0.5),
            ]
        )
        result = rebalance(portfolio, target)
        # sol_symbol not in either portfolio or target
        zero = result[sol_symbol]
        assert zero.delta_market_value == 0.0
        assert zero.current_market_value == 0.0


class TestRebalanceResult:
    def test_empty_to_buy_and_sell(
        self,
        btc_symbol: Symbol,
    ) -> None:
        result = RebalanceResult(
            items=[],
            total_value=0.0,
        )
        assert result.to_buy() == []
        assert result.to_sell() == []
