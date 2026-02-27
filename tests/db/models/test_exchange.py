from xarizmi.db.models.exchange import Exchange
from xarizmi.models.exchange import Exchange as PyExchange


class TestExchangeFromPydantic:
    def test_name_field_is_set(self) -> None:
        py_exc = PyExchange(name="BINANCE")
        db_exc = Exchange.from_pydantic(py_exc)
        assert db_exc.name == "BINANCE"

    def test_different_names(self) -> None:
        for name in ["KRAKEN", "COINBASE", "BYBIT"]:
            db_exc = Exchange.from_pydantic(PyExchange(name=name))
            assert db_exc.name == name


class TestExchangeToPydantic:
    def test_returns_pydantic_exchange(self) -> None:
        db_exc = Exchange(name="COINBASE")
        result = db_exc.to_pydantic()
        assert isinstance(result, PyExchange)

    def test_name_matches(self) -> None:
        db_exc = Exchange(name="KRAKEN")
        result = db_exc.to_pydantic()
        assert result.name == "KRAKEN"


class TestExchangeRoundTrip:
    def test_round_trip_through_db(self, session) -> None:  # type: ignore[no-untyped-def]
        # Given a pydantic Exchange
        py_exc = PyExchange(name="KRAKEN")
        # When we persist it via from_pydantic
        session.add(Exchange.from_pydantic(py_exc))
        session.flush()
        # And convert back via to_pydantic
        fetched = session.get(Exchange, "KRAKEN")
        assert fetched is not None
        result = fetched.to_pydantic()
        # Then the name is preserved
        assert result.name == py_exc.name

    def test_stored_as_pk(self, session) -> None:  # type: ignore[no-untyped-def]
        # Exchange name is the primary key — querying by name works
        session.add(Exchange(name="BYBIT"))
        session.flush()
        fetched = session.get(Exchange, "BYBIT")
        assert fetched is not None
        assert fetched.name == "BYBIT"
