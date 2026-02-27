import pytest
from sqlalchemy.orm import Session

from xarizmi.db.models.order import Order
from xarizmi.db.models.symbol import Symbol
from xarizmi.enums import OrderStatusEnum, SideEnum
from xarizmi.models.orders import Order as PyOrder
from xarizmi.models.symbol import Symbol as PySymbol


@pytest.fixture
def py_order(db_symbol: Symbol) -> PyOrder:
    return PyOrder(
        symbol=PySymbol.build("BTC", "USD", "USD", "BINANCE"),
        price=50000.0,
        amount=0.5,
        status=OrderStatusEnum.ACTIVE,
        side=SideEnum.BUY,
        order_id="order-001",
    )


class TestOrderFromPydantic:
    def test_order_id_is_set(
        self, db_symbol: Symbol, py_order: PyOrder
    ) -> None:
        db_ord = Order.from_pydantic(py_order, symbol_id=db_symbol.id)
        assert db_ord.order_id == "order-001"

    def test_price_is_set(self, db_symbol: Symbol, py_order: PyOrder) -> None:
        db_ord = Order.from_pydantic(py_order, symbol_id=db_symbol.id)
        assert db_ord.price == 50000.0

    def test_amount_is_set(self, db_symbol: Symbol, py_order: PyOrder) -> None:
        db_ord = Order.from_pydantic(py_order, symbol_id=db_symbol.id)
        assert db_ord.amount == 0.5

    def test_side_is_set(self, db_symbol: Symbol, py_order: PyOrder) -> None:
        db_ord = Order.from_pydantic(py_order, symbol_id=db_symbol.id)
        assert db_ord.side == SideEnum.BUY

    def test_status_is_set(self, db_symbol: Symbol, py_order: PyOrder) -> None:
        db_ord = Order.from_pydantic(py_order, symbol_id=db_symbol.id)
        assert db_ord.status == OrderStatusEnum.ACTIVE

    def test_symbol_id_fk_is_set(
        self, db_symbol: Symbol, py_order: PyOrder
    ) -> None:
        db_ord = Order.from_pydantic(py_order, symbol_id=db_symbol.id)
        assert db_ord.symbol_id == db_symbol.id

    def test_null_order_id_stored_as_empty_string(
        self, db_symbol: Symbol
    ) -> None:
        py_ord = PyOrder(
            symbol=PySymbol.build("BTC", "USD", "USD", "BINANCE"),
            price=1.0,
            amount=1.0,
            status=OrderStatusEnum.DONE,
            side=SideEnum.SELL,
            order_id=None,
        )
        db_ord = Order.from_pydantic(py_ord, symbol_id=db_symbol.id)
        assert db_ord.order_id == ""


class TestOrderToPydantic:
    def test_returns_pydantic_order(
        self, session: Session, db_symbol: Symbol, py_order: PyOrder
    ) -> None:
        db_ord = Order.from_pydantic(py_order, symbol_id=db_symbol.id)
        session.add(db_ord)
        session.flush()

        fetched = session.get(Order, db_ord.id)
        assert fetched is not None
        result = fetched.to_pydantic()
        assert isinstance(result, PyOrder)

    def test_price_matches(
        self, session: Session, db_symbol: Symbol, py_order: PyOrder
    ) -> None:
        db_ord = Order.from_pydantic(py_order, symbol_id=db_symbol.id)
        session.add(db_ord)
        session.flush()

        fetched = session.get(Order, db_ord.id)
        assert fetched is not None
        assert fetched.to_pydantic().price == 50000.0

    def test_amount_matches(
        self, session: Session, db_symbol: Symbol, py_order: PyOrder
    ) -> None:
        db_ord = Order.from_pydantic(py_order, symbol_id=db_symbol.id)
        session.add(db_ord)
        session.flush()

        fetched = session.get(Order, db_ord.id)
        assert fetched is not None
        assert fetched.to_pydantic().amount == 0.5

    def test_side_matches(
        self, session: Session, db_symbol: Symbol, py_order: PyOrder
    ) -> None:
        db_ord = Order.from_pydantic(py_order, symbol_id=db_symbol.id)
        session.add(db_ord)
        session.flush()

        fetched = session.get(Order, db_ord.id)
        assert fetched is not None
        assert fetched.to_pydantic().side == SideEnum.BUY

    def test_status_matches(
        self, session: Session, db_symbol: Symbol, py_order: PyOrder
    ) -> None:
        db_ord = Order.from_pydantic(py_order, symbol_id=db_symbol.id)
        session.add(db_ord)
        session.flush()

        fetched = session.get(Order, db_ord.id)
        assert fetched is not None
        assert fetched.to_pydantic().status == OrderStatusEnum.ACTIVE

    def test_symbol_loaded_via_relationship(
        self, session: Session, db_symbol: Symbol, py_order: PyOrder
    ) -> None:
        # The FK symbol_id links to the symbol table;
        # to_pydantic() navigates the relationship to reconstruct the symbol.
        db_ord = Order.from_pydantic(py_order, symbol_id=db_symbol.id)
        session.add(db_ord)
        session.flush()

        fetched = session.get(Order, db_ord.id)
        assert fetched is not None
        result = fetched.to_pydantic()
        assert result.symbol.base_currency.name == "BTC"
        assert result.symbol.quote_currency.name == "USD"
        assert result.symbol.exchange is not None
        assert result.symbol.exchange.name == "BINANCE"


class TestOrderFKRelationship:
    def test_order_symbol_fk_stored(
        self, session: Session, db_symbol: Symbol
    ) -> None:
        db_ord = Order(
            symbol_id=db_symbol.id,
            order_id="fk-test",
            price=100.0,
            amount=1.0,
            side=SideEnum.BUY,
            status=OrderStatusEnum.ACTIVE,
        )
        session.add(db_ord)
        session.flush()

        fetched = session.get(Order, db_ord.id)
        assert fetched is not None
        assert fetched.symbol_id == db_symbol.id

    def test_order_accessible_from_symbol(
        self, session: Session, db_symbol: Symbol
    ) -> None:
        db_ord = Order(
            symbol_id=db_symbol.id,
            order_id="reverse-nav",
            price=200.0,
            amount=2.0,
            side=SideEnum.SELL,
            status=OrderStatusEnum.DONE,
        )
        session.add(db_ord)
        session.flush()
        session.refresh(db_symbol)

        # Traverse the reverse relationship: symbol.orders
        assert any(o.order_id == "reverse-nav" for o in db_symbol.orders)


class TestOrderRoundTrip:
    def test_round_trip_through_db(
        self, session: Session, db_symbol: Symbol
    ) -> None:
        py_ord = PyOrder(
            symbol=PySymbol.build("BTC", "USD", "USD", "BINANCE"),
            price=42000.0,
            amount=1.5,
            status=OrderStatusEnum.DONE,
            side=SideEnum.SELL,
            order_id="rt-001",
        )
        db_ord = Order.from_pydantic(py_ord, symbol_id=db_symbol.id)
        session.add(db_ord)
        session.flush()

        fetched = session.get(Order, db_ord.id)
        assert fetched is not None
        result = fetched.to_pydantic()

        assert result.price == py_ord.price
        assert result.amount == py_ord.amount
        assert result.status == py_ord.status
        assert result.side == py_ord.side
        assert result.order_id == py_ord.order_id
        assert result.symbol.base_currency.name == "BTC"
