from xarizmi.db.models.currency import Currency
from xarizmi.models.currency import Currency as PyCurrency


class TestCurrencyFromPydantic:
    def test_name_field_is_set(self) -> None:
        py_cur = PyCurrency(name="BTC")
        db_cur = Currency.from_pydantic(py_cur)
        assert db_cur.name == "BTC"

    def test_different_names(self) -> None:
        for name in ["ETH", "USDT", "USD"]:
            db_cur = Currency.from_pydantic(PyCurrency(name=name))
            assert db_cur.name == name


class TestCurrencyToPydantic:
    def test_returns_pydantic_currency(self) -> None:
        db_cur = Currency(name="BTC")
        result = db_cur.to_pydantic()
        assert isinstance(result, PyCurrency)

    def test_name_matches(self) -> None:
        db_cur = Currency(name="ETH")
        result = db_cur.to_pydantic()
        assert result.name == "ETH"


class TestCurrencyRoundTrip:
    def test_round_trip_through_db(self, session) -> None:  # type: ignore[no-untyped-def]
        # Given a pydantic Currency
        py_cur = PyCurrency(name="SOL")
        # When persisted via from_pydantic
        session.add(Currency.from_pydantic(py_cur))
        session.flush()
        # And converted back via to_pydantic
        fetched = session.get(Currency, "SOL")
        assert fetched is not None
        result = fetched.to_pydantic()
        # Then name is preserved
        assert result.name == py_cur.name

    def test_stored_as_pk(self, session) -> None:  # type: ignore[no-untyped-def]
        session.add(Currency(name="BNB"))
        session.flush()
        fetched = session.get(Currency, "BNB")
        assert fetched is not None
        assert fetched.name == "BNB"
