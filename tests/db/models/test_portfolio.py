import datetime

import pytest

from xarizmi.db.models.portfolio import Portfolio, PortfolioItem
from xarizmi.models.portfolio import Portfolio as PyPortfolio
from xarizmi.models.portfolio import PortfolioItem as PyPortfolioItem
from xarizmi.models.symbol import Symbol as PySymbol


@pytest.fixture
def snapshot_dt() -> datetime.datetime:
    return datetime.datetime(2024, 11, 26, 12, 0, 0)


@pytest.fixture
def py_portfolio_item(snapshot_dt) -> PyPortfolioItem:  # type: ignore[no-untyped-def]
    return PyPortfolioItem(
        symbol=PySymbol.build("BTC", "USD", "USD", "BINANCE"),
        market_value=80_000.0,
        quantity=1.0,
        datetime=snapshot_dt,
    )


class TestPortfolioItemFromPydantic:
    def test_market_value_is_set(self, db_symbol, py_portfolio_item) -> None:  # type: ignore[no-untyped-def]
        db_item = PortfolioItem.from_pydantic(
            py_portfolio_item, symbol_id=db_symbol.id
        )
        assert db_item.market_value == 80_000.0

    def test_quantity_is_set(self, db_symbol, py_portfolio_item) -> None:  # type: ignore[no-untyped-def]
        db_item = PortfolioItem.from_pydantic(
            py_portfolio_item, symbol_id=db_symbol.id
        )
        assert db_item.quantity == 1.0

    def test_datetime_is_set(
        self, db_symbol, py_portfolio_item, snapshot_dt
    ) -> None:  # type: ignore[no-untyped-def]
        db_item = PortfolioItem.from_pydantic(
            py_portfolio_item, symbol_id=db_symbol.id
        )
        assert db_item.datetime == snapshot_dt

    def test_symbol_id_fk_is_set(self, db_symbol, py_portfolio_item) -> None:  # type: ignore[no-untyped-def]
        db_item = PortfolioItem.from_pydantic(
            py_portfolio_item, symbol_id=db_symbol.id
        )
        assert db_item.symbol_id == db_symbol.id


class TestPortfolioItemToPydantic:
    def test_returns_pydantic_portfolio_item(
        self, session, db_symbol, py_portfolio_item
    ) -> None:  # type: ignore[no-untyped-def]
        db_item = PortfolioItem.from_pydantic(
            py_portfolio_item, symbol_id=db_symbol.id
        )
        session.add(db_item)
        session.flush()

        fetched = session.get(PortfolioItem, db_item.id)
        assert fetched is not None
        result = fetched.to_pydantic()
        assert isinstance(result, PyPortfolioItem)

    def test_market_value_matches(
        self, session, db_symbol, py_portfolio_item
    ) -> None:  # type: ignore[no-untyped-def]
        db_item = PortfolioItem.from_pydantic(
            py_portfolio_item, symbol_id=db_symbol.id
        )
        session.add(db_item)
        session.flush()

        fetched = session.get(PortfolioItem, db_item.id)
        assert fetched is not None
        assert fetched.to_pydantic().market_value == 80_000.0

    def test_quantity_matches(
        self, session, db_symbol, py_portfolio_item
    ) -> None:  # type: ignore[no-untyped-def]
        db_item = PortfolioItem.from_pydantic(
            py_portfolio_item, symbol_id=db_symbol.id
        )
        session.add(db_item)
        session.flush()

        fetched = session.get(PortfolioItem, db_item.id)
        assert fetched is not None
        assert fetched.to_pydantic().quantity == 1.0

    def test_symbol_loaded_via_relationship(
        self, session, db_symbol, py_portfolio_item
    ) -> None:  # type: ignore[no-untyped-def]
        # The FK symbol_id is the DB link; to_pydantic() navigates the
        # symbol relationship to reconstruct the full pydantic Symbol.
        db_item = PortfolioItem.from_pydantic(
            py_portfolio_item, symbol_id=db_symbol.id
        )
        session.add(db_item)
        session.flush()

        fetched = session.get(PortfolioItem, db_item.id)
        assert fetched is not None
        result = fetched.to_pydantic()
        assert result.symbol.base_currency.name == "BTC"
        assert result.symbol.quote_currency.name == "USD"
        assert result.symbol.exchange is not None
        assert result.symbol.exchange.name == "BINANCE"


class TestPortfolioItemFKRelationship:
    def test_item_accessible_from_symbol(
        self, session, db_symbol, snapshot_dt
    ) -> None:  # type: ignore[no-untyped-def]
        db_item = PortfolioItem(
            symbol_id=db_symbol.id,
            market_value=5000.0,
            quantity=2.0,
            datetime=snapshot_dt,
        )
        session.add(db_item)
        session.flush()
        session.refresh(db_symbol)

        # Traverse the reverse relationship: symbol.portfolio_items
        assert any(i.market_value == 5000.0 for i in db_symbol.portfolio_items)


class TestPortfolioFromPydantic:
    def test_datetime_is_set(self, snapshot_dt) -> None:
        py_portfolio = PyPortfolio(
            items=[
                PyPortfolioItem(
                    symbol=PySymbol.build("BTC", "USD", "USD", "BINANCE"),
                    market_value=80_000.0,
                    quantity=1.0,
                    datetime=snapshot_dt,
                )
            ]
        )
        db_portfolio = Portfolio.from_pydantic(py_portfolio)
        assert db_portfolio.datetime == snapshot_dt


class TestPortfolioToPydantic:
    def test_round_trip_with_items(
        self, session, db_symbol, db_eth_symbol, snapshot_dt
    ) -> None:  # type: ignore[no-untyped-def]
        # Given a Portfolio saved with two items
        db_portfolio = Portfolio(datetime=snapshot_dt)
        session.add(db_portfolio)
        session.flush()

        item1 = PortfolioItem(
            symbol_id=db_symbol.id,
            market_value=80_000.0,
            quantity=1.0,
            datetime=snapshot_dt,
            portfolio_id=db_portfolio.id,
        )
        item2 = PortfolioItem(
            symbol_id=db_eth_symbol.id,
            market_value=3_200.0,
            quantity=1.0,
            datetime=snapshot_dt,
            portfolio_id=db_portfolio.id,
        )
        session.add_all([item1, item2])
        session.flush()

        # When converting back to pydantic
        fetched = session.get(Portfolio, db_portfolio.id)
        assert fetched is not None
        result = fetched.to_pydantic()

        # Then we get a valid Portfolio with both items
        assert isinstance(result, PyPortfolio)
        assert len(result.items) == 2

    def test_portfolio_items_have_correct_symbols(
        self, session, db_symbol, db_eth_symbol, snapshot_dt
    ) -> None:  # type: ignore[no-untyped-def]
        db_portfolio = Portfolio(datetime=snapshot_dt)
        session.add(db_portfolio)
        session.flush()

        session.add(
            PortfolioItem(
                symbol_id=db_symbol.id,
                market_value=80_000.0,
                quantity=1.0,
                datetime=snapshot_dt,
                portfolio_id=db_portfolio.id,
            )
        )
        session.flush()

        fetched = session.get(Portfolio, db_portfolio.id)
        assert fetched is not None
        result = fetched.to_pydantic()
        assert result.items[0].symbol.base_currency.name == "BTC"

    def test_portfolio_item_portfolio_id_fk(
        self, session, db_symbol, snapshot_dt
    ) -> None:  # type: ignore[no-untyped-def]
        # A PortfolioItem may optionally reference a Portfolio
        # via portfolio_id FK.
        db_portfolio = Portfolio(datetime=snapshot_dt)
        session.add(db_portfolio)
        session.flush()

        db_item = PortfolioItem(
            symbol_id=db_symbol.id,
            market_value=1_000.0,
            quantity=0.1,
            datetime=snapshot_dt,
            portfolio_id=db_portfolio.id,
        )
        session.add(db_item)
        session.flush()

        fetched_item = session.get(PortfolioItem, db_item.id)
        assert fetched_item is not None
        assert fetched_item.portfolio_id == db_portfolio.id

    def test_portfolio_item_without_portfolio_id(
        self, session, db_symbol, snapshot_dt
    ) -> None:  # type: ignore[no-untyped-def]
        # portfolio_id is optional — items can exist without a parent
        # Portfolio.
        db_item = PortfolioItem(
            symbol_id=db_symbol.id,
            market_value=500.0,
            quantity=0.5,
            datetime=snapshot_dt,
            portfolio_id=None,
        )
        session.add(db_item)
        session.flush()

        fetched = session.get(PortfolioItem, db_item.id)
        assert fetched is not None
        assert fetched.portfolio_id is None


class TestPortfolioRoundTrip:
    def test_round_trip_through_db(
        self, session, db_symbol, snapshot_dt
    ) -> None:  # type: ignore[no-untyped-def]
        py_portfolio = PyPortfolio(
            items=[
                PyPortfolioItem(
                    symbol=PySymbol.build("BTC", "USD", "USD", "BINANCE"),
                    market_value=60_000.0,
                    quantity=1.0,
                    datetime=snapshot_dt,
                )
            ]
        )
        # Persist Portfolio header
        db_portfolio = Portfolio.from_pydantic(py_portfolio)
        session.add(db_portfolio)
        session.flush()

        # Persist items, linking to portfolio via FK
        for item in py_portfolio.items:
            db_item = PortfolioItem.from_pydantic(item, symbol_id=db_symbol.id)
            db_item.portfolio_id = db_portfolio.id
            session.add(db_item)
        session.flush()

        # Fetch and convert back
        fetched = session.get(Portfolio, db_portfolio.id)
        assert fetched is not None
        result = fetched.to_pydantic()

        assert len(result.items) == 1
        assert result.items[0].market_value == 60_000.0
        assert result.items[0].symbol.base_currency.name == "BTC"
