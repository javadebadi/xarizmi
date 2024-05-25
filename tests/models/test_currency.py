from xarizmi.models.currency import Currency


class TestCurrency:

    def test(self) -> None:
        currency = Currency(name="USD")
        assert currency.name == "USD"
        assert currency.model_dump() == {"name": "USD"}
