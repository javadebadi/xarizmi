from xarizmi.models.currency import Currency
from xarizmi.models.symbol import Symbol


class TestSymbol:

    def test(self) -> None:
        symbol = Symbol(
            base_currency=Currency(name="BTC"),
            quote_currency=Currency(name="USD"),
            fee_currency=Currency(name="USD"),
        )
        assert symbol.model_dump() == {
            "base_currency": {
                "name": "BTC",
            },
            "fee_currency": {
                "name": "USD",
            },
            "quote_currency": {
                "name": "USD",
            },
        }

    def test_build(self) -> None:
        symbol = Symbol.build(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
        )
        assert symbol.model_dump() == {
            "base_currency": {
                "name": "BTC",
            },
            "fee_currency": {
                "name": "USD",
            },
            "quote_currency": {
                "name": "USD",
            },
        }
