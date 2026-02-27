from datetime import datetime as dt
from typing import Optional, Self

from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from xarizmi.db.models.base import Base
from xarizmi.models.portfolio import Portfolio as PyPortfolio
from xarizmi.models.portfolio import PortfolioItem as PyPortfolioItem

from .constants import TableNamesEnum
from .symbol import Symbol


class Portfolio(Base):  # type: ignore
    __tablename__ = TableNamesEnum.PORTFOLIO.value
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    datetime: Mapped[dt] = mapped_column(DateTime, nullable=False, unique=True)

    items: Mapped[list["PortfolioItem"]] = relationship(
        "PortfolioItem", back_populates="portfolio"
    )

    def to_pydantic(self) -> PyPortfolio:
        return PyPortfolio(items=[item.to_pydantic() for item in self.items])

    @classmethod
    def from_pydantic(cls, portfolio: PyPortfolio) -> Self:
        return cls(datetime=portfolio.portfolio_datetime)


class PortfolioItem(Base):  # type: ignore
    __tablename__ = TableNamesEnum.PORTFOLIO_ITEM.value
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    symbol_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Symbol.id), nullable=False
    )
    symbol: Mapped[Symbol] = relationship(
        "Symbol", back_populates="portfolio_items"
    )

    portfolio_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey(Portfolio.id), nullable=True
    )
    portfolio: Mapped[Optional[Portfolio]] = relationship(
        "Portfolio", back_populates="items"
    )

    market_value: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    datetime: Mapped[dt] = mapped_column(
        DateTime,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "symbol_id",
            "datetime",
            name="uix_symbol_datetime",
        ),
    )

    def to_pydantic(self) -> PyPortfolioItem:
        return PyPortfolioItem(
            symbol=self.symbol.to_pydantic(),
            market_value=float(self.market_value),
            quantity=float(self.quantity),
            datetime=self.datetime,
        )

    @classmethod
    def from_pydantic(cls, item: PyPortfolioItem, symbol_id: int) -> Self:
        return cls(
            symbol_id=symbol_id,
            market_value=item.market_value,
            quantity=item.quantity,
            datetime=item.datetime,
        )
