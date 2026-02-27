from xarizmi.enums import OrderStatusEnum, SideEnum
from xarizmi.models.currency import Currency
from xarizmi.models.orders import Order
from xarizmi.models.symbol import Symbol


class TestOrder:
    def test_build_from_currencies(self) -> None:
        order = Order.build_from_currencies(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            order_id="12345",
            price=75000,
            amount=1,
            status=OrderStatusEnum.ACTIVE,
            side=SideEnum.BUY,
            exchange="BINANCE",
        )
        assert order.price == 75000
        assert order.amount == 1
        assert order.order_id == "12345"
        assert order.symbol.base_currency.name == "BTC"
        assert order.symbol.exchange is not None
        assert order.symbol.exchange.name == "BINANCE"

    def test(self) -> None:
        symbol = Symbol(
            base_currency=Currency(name="BTC"),
            quote_currency=Currency(name="USD"),
            fee_currency=Currency(name="USD"),
        )
        order = Order(
            symbol=symbol,
            price=75000,
            amount=1,
            status=OrderStatusEnum.ACTIVE,
            side=SideEnum.BUY,
        )

        assert order.model_dump()["amount"] == 1.0
        assert order.model_dump()["price"] == 75000.0
        assert order.model_dump()["side"] == SideEnum.BUY
        assert order.model_dump()["status"] == OrderStatusEnum.ACTIVE
        assert order.model_dump()["symbol"] == symbol.model_dump()
