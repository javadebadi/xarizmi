from xarizmi.models.exchange import Exchange, ExchangeList


class TestExchange:
    def test(self) -> None:
        exchange = Exchange(name="BINANCE")
        assert exchange.name == "BINANCE"

    def test_to_string(self) -> None:
        exchange = Exchange(name="BINANCE")
        assert exchange.to_string() == "BINANCE"

    def test_eq(self) -> None:
        assert Exchange(name="BINANCE") == Exchange(name="BINANCE")
        assert Exchange(name="BINANCE") != Exchange(name="COINBASE")

    def test_eq_with_non_exchange_returns_not_implemented(self) -> None:
        exchange = Exchange(name="BINANCE")
        assert exchange.__eq__("BINANCE") is NotImplemented

    def test_hash(self) -> None:
        exchange = Exchange(name="BINANCE")
        assert hash(exchange) == hash("BINANCE")
        assert len({Exchange(name="BINANCE"), Exchange(name="COINBASE")}) == 2


class TestExchangeList:
    def test(self) -> None:
        exchanges = ExchangeList(
            items=[Exchange(name="BINANCE"), Exchange(name="COINBASE")]
        )
        assert len(exchanges.items) == 2
