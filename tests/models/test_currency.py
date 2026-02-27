from xarizmi.models.currency import Currency


class TestCurrency:
    def test(self) -> None:
        currency = Currency(name="USD")
        assert currency.name == "USD"

    def test_to_string(self) -> None:
        currency = Currency(name="USD")
        assert currency.to_string() == "USD"

    def test_eq_with_non_currency_returns_not_implemented(self) -> None:
        currency = Currency(name="USD")
        assert currency.__eq__("USD") is NotImplemented

    def test_hash(self) -> None:
        currency = Currency(name="USD")
        assert hash(currency) == hash("USD")
        assert len({Currency(name="USD"), Currency(name="EUR")}) == 2
