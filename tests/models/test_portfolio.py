import datetime

import pytest

from xarizmi.models.portfolio import Portfolio
from xarizmi.models.portfolio import PortfolioItem
from xarizmi.models.portfolio import PortfolioItemDifference
from xarizmi.models.portfolio import PortfolioItemRatio
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
