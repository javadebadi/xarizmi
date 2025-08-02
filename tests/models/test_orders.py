from xarizmi.enums import OrderStatusEnum
from xarizmi.enums import SideEnum
from xarizmi.models.currency import Currency
from xarizmi.models.orders import Order
from xarizmi.models.symbol import Symbol


class TestOrder:

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
