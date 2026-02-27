from sqlalchemy.orm import joinedload

from xarizmi.db.models.exchange import Exchange
from xarizmi.db.models.symbol import Symbol
from xarizmi.models.symbol import Symbol as PySymbol


class TestSymbolFromPydantic:
    def test_base_currency_is_set(self) -> None:
        py_sym = PySymbol.build("BTC", "USD", "USD", "BINANCE")
        db_sym = Symbol.from_pydantic(py_sym)
        assert db_sym.base_currency == "BTC"

    def test_quote_currency_is_set(self) -> None:
        py_sym = PySymbol.build("BTC", "USD", "USD", "BINANCE")
        db_sym = Symbol.from_pydantic(py_sym)
        assert db_sym.quote_currency == "USD"

    def test_fee_currency_is_set(self) -> None:
        py_sym = PySymbol.build("BTC", "USD", "USD", "BINANCE")
        db_sym = Symbol.from_pydantic(py_sym)
        assert db_sym.fee_currency == "USD"

    def test_exchange_name_is_set(self) -> None:
        py_sym = PySymbol.build("BTC", "USD", "USD", "BINANCE")
        db_sym = Symbol.from_pydantic(py_sym)
        assert db_sym.exchange_name == "BINANCE"

    def test_exchange_name_none_when_no_exchange(self) -> None:
        py_sym = PySymbol.build("BTC", "USD", "USD")
        db_sym = Symbol.from_pydantic(py_sym)
        assert db_sym.exchange_name is None


class TestSymbolToPydantic:
    def test_returns_pydantic_symbol(self) -> None:
        db_sym = Symbol(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            exchange_name="BINANCE",
        )
        result = db_sym.to_pydantic()
        assert isinstance(result, PySymbol)

    def test_base_currency_name(self) -> None:
        db_sym = Symbol(
            base_currency="ETH",
            quote_currency="USDT",
            fee_currency="USDT",
            exchange_name="KRAKEN",
        )
        result = db_sym.to_pydantic()
        assert result.base_currency.name == "ETH"

    def test_quote_currency_name(self) -> None:
        db_sym = Symbol(
            base_currency="ETH",
            quote_currency="USDT",
            fee_currency="USDT",
            exchange_name="KRAKEN",
        )
        result = db_sym.to_pydantic()
        assert result.quote_currency.name == "USDT"

    def test_fee_currency_name(self) -> None:
        db_sym = Symbol(
            base_currency="ETH",
            quote_currency="USDT",
            fee_currency="BNB",
            exchange_name="KRAKEN",
        )
        result = db_sym.to_pydantic()
        assert result.fee_currency.name == "BNB"

    def test_exchange_name(self) -> None:
        db_sym = Symbol(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            exchange_name="COINBASE",
        )
        result = db_sym.to_pydantic()
        assert result.exchange is not None
        assert result.exchange.name == "COINBASE"

    def test_exchange_is_none_when_not_set(self) -> None:
        db_sym = Symbol(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            exchange_name=None,
        )
        result = db_sym.to_pydantic()
        assert result.exchange is None


class TestSymbolFKRelationship:
    def test_symbol_fk_references_exchange(self, session) -> None:  # type: ignore[no-untyped-def]
        # Given an exchange and a symbol persisted with that FK
        exc = Exchange(name="BINANCE")
        session.add(exc)
        session.flush()

        sym = Symbol(
            base_currency="BTC",
            quote_currency="USD",
            fee_currency="USD",
            exchange_name="BINANCE",
        )
        session.add(sym)
        session.flush()

        # When fetching back with the exchange relationship
        fetched = (
            session.query(Symbol)
            .options(joinedload(Symbol.exchange))
            .filter_by(base_currency="BTC", quote_currency="USD")
            .first()
        )
        assert fetched is not None
        assert fetched.exchange_name == "BINANCE"
        assert fetched.exchange.name == "BINANCE"

    def test_symbol_exchange_relationship_navigable(self, session) -> None:  # type: ignore[no-untyped-def]
        exc = Exchange(name="BYBIT")
        session.add(exc)
        session.flush()

        sym = Symbol(
            base_currency="SOL",
            quote_currency="USD",
            fee_currency="USD",
            exchange_name="BYBIT",
        )
        session.add(sym)
        session.flush()

        fetched_exc = session.get(Exchange, "BYBIT")
        assert fetched_exc is not None
        # Traverse the reverse relationship: exchange.symbols
        assert any(s.base_currency == "SOL" for s in fetched_exc.symbols)


class TestSymbolRoundTrip:
    def test_round_trip_through_db(self, session) -> None:  # type: ignore[no-untyped-def]
        # Given an exchange in DB
        session.add(Exchange(name="BINANCE"))
        session.flush()

        # And a pydantic symbol
        py_sym = PySymbol.build("BTC", "USD", "USD", "BINANCE")

        # When we persist via from_pydantic
        session.add(Symbol.from_pydantic(py_sym))
        session.flush()

        # And convert back via to_pydantic
        fetched = (
            session.query(Symbol)
            .filter_by(base_currency="BTC", exchange_name="BINANCE")
            .first()
        )
        assert fetched is not None
        result = fetched.to_pydantic()

        assert result.base_currency.name == py_sym.base_currency.name
        assert result.quote_currency.name == py_sym.quote_currency.name
        assert result.fee_currency.name == py_sym.fee_currency.name
        assert result.exchange is not None
        assert result.exchange.name == "BINANCE"
