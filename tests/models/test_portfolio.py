import datetime

import pytest

from xarizmi.models.portfolio import (
    Portfolio,
    PortfolioDifference,
    PortfolioItem,
    PortfolioItemDifference,
    PortfolioItemRatio,
    PortfolioRatio,
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
def cro_symbol() -> Symbol:
    return Symbol.build(
        base_currency="CRO",
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


class TestPortfolio:
    def test_different_datetimes_in_portfolio_items(
        self, btc_symbol: Symbol, eth_symbol: Symbol
    ) -> None:
        # Given portfolio items in different datetimes
        items = [
            PortfolioItem(
                symbol=btc_symbol,
                market_value=100000,
                quantity=1,
                datetime=datetime.datetime(2024, 11, 26),
            ),
            PortfolioItem(
                symbol=eth_symbol,
                market_value=3000,
                quantity=1,
                datetime=datetime.datetime(2024, 11, 1),
            ),
        ]
        # When Portfolio object is created
        # I should see the ValueError is raised
        with pytest.raises(ValueError):
            Portfolio(items=items)

    def test_getitem(self, btc_symbol: Symbol, eth_symbol: Symbol) -> None:
        # Given portfolio items and portfolio created by them
        items = [
            PortfolioItem(
                symbol=btc_symbol,
                market_value=100000,
                quantity=1,
                datetime=datetime.datetime(2024, 11, 26),
            ),
            PortfolioItem(
                symbol=eth_symbol,
                market_value=3000,
                quantity=1,
                datetime=datetime.datetime(2024, 11, 26),
            ),
        ]
        portfolio = Portfolio(items=items)
        # When I access the portfolio item using [symbol] syntax
        # I should see correct portfolio_item
        assert portfolio[btc_symbol] == items[0]
        assert portfolio[eth_symbol] == items[1]

    def test_getitem_with_non_existing_symbol(
        self, btc_symbol: Symbol, eth_symbol: Symbol
    ) -> None:
        # Given portfolio items and portfolio created by them
        items = [
            PortfolioItem(
                symbol=btc_symbol,
                market_value=100000,
                quantity=1,
                datetime=datetime.datetime(2024, 11, 26),
            ),
        ]
        portfolio = Portfolio(items=items)
        # When I access the portfolio item using [symbol] syntax
        # for a symbol that is not in portfolio
        # I should see correct portfolio_item
        assert portfolio[eth_symbol].datetime == portfolio.portfolio_datetime
        assert portfolio[eth_symbol].market_value == 0
        assert portfolio[eth_symbol].quantity == 0
        assert portfolio[eth_symbol].symbol == eth_symbol

    def test___sub__(
        self, btc_symbol: Symbol, eth_symbol: Symbol, cro_symbol: Symbol
    ) -> None:
        # Given portfolio items and portfolio created by them
        items = [
            PortfolioItem(
                symbol=btc_symbol,
                market_value=100000,
                quantity=1,
                datetime=datetime.datetime(2024, 11, 26),
            ),
            PortfolioItem(
                symbol=eth_symbol,
                market_value=3000,
                quantity=1,
                datetime=datetime.datetime(2024, 11, 26),
            ),
        ]
        portfolio = Portfolio(items=items)
        # And another portfolio
        other_items = [
            PortfolioItem(
                symbol=btc_symbol,
                market_value=50000,
                quantity=1,
                datetime=datetime.datetime(2023, 11, 26),
            ),
            PortfolioItem(
                symbol=eth_symbol,
                market_value=1500,
                quantity=1,
                datetime=datetime.datetime(2023, 11, 26),
            ),
            PortfolioItem(
                symbol=cro_symbol,
                market_value=1000,
                quantity=10000,
                datetime=datetime.datetime(2023, 11, 26),
            ),
        ]
        other_portfolio = Portfolio(items=other_items)
        # When I subtract portfolios I will have
        assert (portfolio - other_portfolio)[
            btc_symbol
        ] == PortfolioItemDifference(
            symbol=btc_symbol,
            delta_market_value=50000,
            delta_quantity=0,
            delta_datetime=datetime.timedelta(days=366),
        )
        assert (portfolio - other_portfolio)[
            eth_symbol
        ] == PortfolioItemDifference(
            symbol=eth_symbol,
            delta_market_value=1500,
            delta_quantity=0,
            delta_datetime=datetime.timedelta(days=366),
        )
        assert (portfolio - other_portfolio)[
            cro_symbol
        ] == PortfolioItemDifference(
            symbol=cro_symbol,
            delta_market_value=-1000,
            delta_quantity=-10000,
            delta_datetime=datetime.timedelta(days=366),
        )

    def test___truediv__(
        self, btc_symbol: Symbol, eth_symbol: Symbol, cro_symbol: Symbol
    ) -> None:
        # Given portfolio items and portfolio created by them
        items = [
            PortfolioItem(
                symbol=btc_symbol,
                market_value=100000,
                quantity=1,
                datetime=datetime.datetime(2024, 11, 26),
            ),
            PortfolioItem(
                symbol=eth_symbol,
                market_value=3000,
                quantity=1,
                datetime=datetime.datetime(2024, 11, 26),
            ),
        ]
        # And another portfolio
        portfolio = Portfolio(items=items)
        other_items = [
            PortfolioItem(
                symbol=btc_symbol,
                market_value=50000,
                quantity=1,
                datetime=datetime.datetime(2023, 11, 26),
            ),
            PortfolioItem(
                symbol=eth_symbol,
                market_value=1500,
                quantity=1,
                datetime=datetime.datetime(2023, 11, 26),
            ),
            PortfolioItem(
                symbol=cro_symbol,
                market_value=1000,
                quantity=10000,
                datetime=datetime.datetime(2023, 11, 26),
            ),
        ]
        other_portfolio = Portfolio(items=other_items)
        # When I divide portfolios I will have
        assert (portfolio / other_portfolio)[btc_symbol] == PortfolioItemRatio(
            symbol=btc_symbol,
            market_value_ratio=2.0,
            quantity_ratio=1.0,
            datetime_ratio_in_days=366.0,
        )
        assert (portfolio / other_portfolio)[eth_symbol] == PortfolioItemRatio(
            symbol=eth_symbol,
            market_value_ratio=2.0,
            quantity_ratio=1.0,
            datetime_ratio_in_days=366.0,
        )
        assert (portfolio / other_portfolio)[cro_symbol] == PortfolioItemRatio(
            symbol=cro_symbol,
            market_value_ratio=0.0,
            quantity_ratio=0.0,
            datetime_ratio_in_days=366.0,
        )


class TestPortfolioItem:
    def test_eq_with_non_portfolio_item_returns_not_implemented(
        self, btc_symbol: Symbol
    ) -> None:
        item = PortfolioItem(
            symbol=btc_symbol,
            market_value=100000,
            quantity=1,
            datetime=datetime.datetime(2024, 11, 26),
        )
        assert item.__eq__("not a portfolio item") is NotImplemented


class TestPortfolioItemRatio:
    def test_return_ratio(self, btc_symbol: Symbol) -> None:
        ratio = PortfolioItemRatio(
            symbol=btc_symbol,
            market_value_ratio=3.0,
            quantity_ratio=1.5,
            datetime_ratio_in_days=30.0,
        )
        assert ratio.return_ratio == 2.0

    def test_return_ratio_zero_quantity_does_not_crash(
        self, btc_symbol: Symbol
    ) -> None:
        ratio = PortfolioItemRatio(
            symbol=btc_symbol,
            market_value_ratio=0.0,
            quantity_ratio=0.0,
            datetime_ratio_in_days=30.0,
        )
        import math

        assert math.isinf(ratio.return_ratio)


class TestPortfolioRatio:
    def _make_ratio(
        self, btc_symbol: Symbol, eth_symbol: Symbol
    ) -> PortfolioRatio:
        return PortfolioRatio(
            items=[
                PortfolioItemRatio(
                    symbol=btc_symbol,
                    market_value_ratio=2.0,
                    quantity_ratio=1.0,
                    datetime_ratio_in_days=366.0,
                ),
                PortfolioItemRatio(
                    symbol=eth_symbol,
                    market_value_ratio=2.0,
                    quantity_ratio=1.0,
                    datetime_ratio_in_days=366.0,
                ),
            ]
        )

    def test_portfolio_datetime_ratio_in_days(
        self, btc_symbol: Symbol, eth_symbol: Symbol
    ) -> None:
        ratio = self._make_ratio(btc_symbol, eth_symbol)
        assert ratio.portfolio_datetime_ratio_in_days == 366.0

    def test_len(self, btc_symbol: Symbol, eth_symbol: Symbol) -> None:
        ratio = self._make_ratio(btc_symbol, eth_symbol)
        assert len(ratio) == 2

    def test_getitem_not_found_returns_default(
        self, btc_symbol: Symbol, eth_symbol: Symbol, sol_symbol: Symbol
    ) -> None:
        ratio = self._make_ratio(btc_symbol, eth_symbol)
        default = ratio[sol_symbol]
        assert default.market_value_ratio == 1
        assert default.quantity_ratio == 1
        assert default.datetime_ratio_in_days == 366.0

    def test_empty_items_allowed(self) -> None:
        ratio = PortfolioRatio(items=[])
        assert len(ratio) == 0

    def test_mismatched_datetime_ratio_raises(
        self, btc_symbol: Symbol, eth_symbol: Symbol
    ) -> None:
        with pytest.raises(ValueError):
            PortfolioRatio(
                items=[
                    PortfolioItemRatio(
                        symbol=btc_symbol,
                        market_value_ratio=2.0,
                        quantity_ratio=1.0,
                        datetime_ratio_in_days=366.0,
                    ),
                    PortfolioItemRatio(
                        symbol=eth_symbol,
                        market_value_ratio=2.0,
                        quantity_ratio=1.0,
                        datetime_ratio_in_days=100.0,
                    ),
                ]
            )


class TestPortfolioDifference:
    def _make_difference(
        self, btc_symbol: Symbol, eth_symbol: Symbol
    ) -> PortfolioDifference:
        return PortfolioDifference(
            items=[
                PortfolioItemDifference(
                    symbol=btc_symbol,
                    delta_market_value=50000,
                    delta_quantity=0,
                    delta_datetime=datetime.timedelta(days=366),
                ),
                PortfolioItemDifference(
                    symbol=eth_symbol,
                    delta_market_value=1500,
                    delta_quantity=0,
                    delta_datetime=datetime.timedelta(days=366),
                ),
            ]
        )

    def test_portfolio_difference_delta_datetime(
        self, btc_symbol: Symbol, eth_symbol: Symbol, sol_symbol: Symbol
    ) -> None:
        diff = self._make_difference(btc_symbol, eth_symbol)
        assert diff.portfolio_difference_delta_datetime == datetime.timedelta(
            days=366
        )

    def test_getitem_not_found_returns_default(
        self, btc_symbol: Symbol, eth_symbol: Symbol, sol_symbol: Symbol
    ) -> None:
        diff = self._make_difference(btc_symbol, eth_symbol)
        default = diff[sol_symbol]
        assert default.delta_market_value == 0
        assert default.delta_quantity == 0
        assert default.delta_datetime == datetime.timedelta(days=366)

    def test_empty_items_allowed(self) -> None:
        diff = PortfolioDifference(items=[])
        assert len(diff.items) == 0

    def test_mismatched_delta_datetime_raises(
        self, btc_symbol: Symbol, eth_symbol: Symbol
    ) -> None:
        with pytest.raises(ValueError):
            PortfolioDifference(
                items=[
                    PortfolioItemDifference(
                        symbol=btc_symbol,
                        delta_market_value=50000,
                        delta_quantity=0,
                        delta_datetime=datetime.timedelta(days=366),
                    ),
                    PortfolioItemDifference(
                        symbol=eth_symbol,
                        delta_market_value=1500,
                        delta_quantity=0,
                        delta_datetime=datetime.timedelta(days=100),
                    ),
                ]
            )


class TestPortfolioAdd:
    def test___add__(self, btc_symbol: Symbol, eth_symbol: Symbol) -> None:
        items = [
            PortfolioItem(
                symbol=btc_symbol,
                market_value=100000,
                quantity=1,
                datetime=datetime.datetime(2024, 11, 26),
            ),
            PortfolioItem(
                symbol=eth_symbol,
                market_value=3000,
                quantity=1,
                datetime=datetime.datetime(2024, 11, 26),
            ),
        ]
        portfolio = Portfolio(items=items)
        diff = PortfolioDifference(
            items=[
                PortfolioItemDifference(
                    symbol=btc_symbol,
                    delta_market_value=10000,
                    delta_quantity=0,
                    delta_datetime=datetime.timedelta(days=1),
                ),
                PortfolioItemDifference(
                    symbol=eth_symbol,
                    delta_market_value=500,
                    delta_quantity=0,
                    delta_datetime=datetime.timedelta(days=1),
                ),
            ]
        )
        result = portfolio + diff
        assert result[btc_symbol].market_value == 110000
        assert result[eth_symbol].market_value == 3500
        assert result[btc_symbol].datetime == datetime.datetime(2024, 11, 27)


class TestPortfolioEmpty:
    def test_empty_portfolio_raises(self) -> None:
        with pytest.raises(ValueError):
            Portfolio(items=[])
