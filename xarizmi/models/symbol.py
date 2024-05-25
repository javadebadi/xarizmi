from pydantic import BaseModel

from xarizmi.models.currency import Currency


class Symbol(BaseModel):
    base_currency: Currency
    quote_currency: Currency
    fee_currency: Currency

    @classmethod
    def build(
        cls, base_currency: str, quote_currency: str, fee_currency: str
    ) -> "Symbol":
        """
        Example
        -------
        >>> symbol = Symbol.build(base_currency="BTC", quote_currency="USD")
        """
        return cls(
            **{
                "base_currency": {"name": base_currency},
                "quote_currency": {"name": quote_currency},
                "fee_currency": {"name": fee_currency},
            }
        )

    def to_string(self) -> str:
        return (
            self.base_currency.to_string()
            + "-"
            + self.quote_currency.to_string()
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "base_currency": self.base_currency.to_string(),
            "quote_currency": self.quote_currency.to_string(),
            "fee_currency": self.fee_currency.to_string(),
        }
