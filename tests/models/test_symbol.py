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
            "exchange": None,
        }

    def test_build(self) -> None:
        symbol = Symbol.build(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            exchange="BINANCE",
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
            "exchange": {"name": "BINANCE"},
        }

    def test_to_string(self) -> None:
        symbol = Symbol.build(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            exchange=None,
        )
        assert symbol.to_string() == "BTC-USD"

    def test_to_dict(self) -> None:
        symbol = Symbol.build(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            exchange=None,
        )
        assert symbol.to_dict() == {
            "base_currency": "BTC",
            "quote_currency": "USD",
            "fee_currency": "USD",
            "exchange": None,
        }

    def test_to_dict_with_exchange(self) -> None:
        symbol = Symbol.build(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            exchange="BINANCE",
        )
        assert symbol.to_dict() == {
            "base_currency": "BTC",
            "quote_currency": "USD",
            "fee_currency": "USD",
            "exchange": "BINANCE",
        }

    def test___eq__(self) -> None:
        symbol = Symbol.build(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            exchange="BINANCE",
        )
        other = Symbol.build(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            exchange="BINANCE",
        )
        assert symbol == other

    def test___eq___when_they_are_not_equal(self) -> None:
        symbol = Symbol.build(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            exchange="BINANCE",
        )
        other = Symbol.build(
            base_currency="CRO",
            quote_currency="USD",
            fee_currency="USD",
            exchange="BINANCE",
        )
        assert symbol != other

    def test_symbols_are_hashable(self) -> None:
        symbol = Symbol.build(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            exchange="BINANCE",
        )
        other = Symbol.build(
            base_currency="CRO",
            quote_currency="USD",
            fee_currency="USD",
            exchange="BINANCE",
        )
        assert set([symbol, other])
