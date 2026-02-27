from typing import Self

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Computed, UniqueConstraint

from xarizmi.db.models.base import Base
from xarizmi.models.currency import Currency as PyCurrency
from xarizmi.models.exchange import Exchange as PyExchange
from xarizmi.models.symbol import Symbol as PySymbol

from .constants import TableNamesEnum
from .exchange import Exchange


class Symbol(Base):  # type: ignore
    __tablename__ = TableNamesEnum.SYMBOL.value
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    base_currency: Mapped[str] = mapped_column(String, nullable=False)
    quote_currency: Mapped[str] = mapped_column(String, nullable=False)
    fee_currency: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(
        String, Computed("base_currency || '-' || quote_currency"), unique=True
    )
    exchange_name: Mapped[str] = mapped_column(
        String, ForeignKey(Exchange.name), nullable=False
    )

    # Establish a many-to-one relationship
    exchange: Mapped[Exchange] = relationship(
        "Exchange", back_populates="symbols"
    )

    candlesticks: Mapped[list["CandleStick"]] = relationship(  # type: ignore  # noqa: F821,E501
        "CandleStick", back_populates="symbol"
    )

    portfolio_items: Mapped[list["PortfolioItem"]] = relationship(  # type: ignore  # noqa: F821,E501
        "PortfolioItem", back_populates="symbol"
    )

    orders: Mapped[list["Order"]] = relationship(  # type: ignore  # noqa: F821,E501
        "Order", back_populates="symbol"
    )

    @property
    def symbol(self) -> str:
        return f"{self.base_currency}-{self.quote_currency}"

    def to_pydantic(self) -> PySymbol:
        return PySymbol(
            base_currency=PyCurrency(name=str(self.base_currency)),
            quote_currency=PyCurrency(name=str(self.quote_currency)),
            fee_currency=PyCurrency(name=str(self.fee_currency)),
            exchange=(
                PyExchange(name=str(self.exchange_name))
                if self.exchange_name
                else None
            ),
        )

    @classmethod
    def from_pydantic(cls, symbol: PySymbol) -> Self:
        return cls(
            base_currency=symbol.base_currency.name,
            quote_currency=symbol.quote_currency.name,
            fee_currency=symbol.fee_currency.name,
            exchange_name=symbol.exchange.name if symbol.exchange else None,
        )

    __table_args__ = (
        UniqueConstraint(
            "base_currency",
            "quote_currency",
            "exchange_name",
            name="uix_symbol_name_exchange",
        ),
    )
