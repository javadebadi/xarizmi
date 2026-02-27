from typing import Self

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from xarizmi.db.models.base import Base
from xarizmi.models.rebalance import (
    PortfolioAllocation as PyPortfolioAllocation,
)
from xarizmi.models.rebalance import (
    PortfolioAllocationItem as PyPortfolioAllocationItem,
)
from xarizmi.models.rebalance import RebalanceItem as PyRebalanceItem
from xarizmi.models.rebalance import RebalanceResult as PyRebalanceResult

from .constants import TableNamesEnum
from .symbol import Symbol


class PortfolioAllocation(Base):  # type: ignore
    __tablename__ = TableNamesEnum.PORTFOLIO_ALLOCATION.value
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    items: Mapped[list["PortfolioAllocationItem"]] = relationship(
        "PortfolioAllocationItem", back_populates="allocation"
    )

    def to_pydantic(self) -> PyPortfolioAllocation:
        return PyPortfolioAllocation(
            items=[item.to_pydantic() for item in self.items]
        )

    @classmethod
    def from_pydantic(cls, allocation: PyPortfolioAllocation) -> Self:
        return cls()


class PortfolioAllocationItem(Base):  # type: ignore
    __tablename__ = TableNamesEnum.PORTFOLIO_ALLOCATION_ITEM.value
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    allocation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(PortfolioAllocation.id), nullable=False
    )
    allocation: Mapped[PortfolioAllocation] = relationship(
        "PortfolioAllocation", back_populates="items"
    )

    symbol_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Symbol.id), nullable=False
    )
    symbol: Mapped[Symbol] = relationship("Symbol")

    weight: Mapped[float] = mapped_column(Float, nullable=False)

    def to_pydantic(self) -> PyPortfolioAllocationItem:
        return PyPortfolioAllocationItem(
            symbol=self.symbol.to_pydantic(),
            weight=float(self.weight),
        )

    @classmethod
    def from_pydantic(
        cls,
        item: PyPortfolioAllocationItem,
        symbol_id: int,
        allocation_id: int,
    ) -> Self:
        return cls(
            symbol_id=symbol_id,
            allocation_id=allocation_id,
            weight=item.weight,
        )


class RebalanceResult(Base):  # type: ignore
    __tablename__ = TableNamesEnum.REBALANCE_RESULT.value
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_value: Mapped[float] = mapped_column(Float, nullable=False)

    items: Mapped[list["RebalanceItem"]] = relationship(
        "RebalanceItem", back_populates="result"
    )

    def to_pydantic(self) -> PyRebalanceResult:
        return PyRebalanceResult(
            items=[item.to_pydantic() for item in self.items],
            total_value=float(self.total_value),
        )

    @classmethod
    def from_pydantic(cls, result: PyRebalanceResult) -> Self:
        return cls(total_value=result.total_value)


class RebalanceItem(Base):  # type: ignore
    __tablename__ = TableNamesEnum.REBALANCE_ITEM.value
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    result_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(RebalanceResult.id), nullable=False
    )
    result: Mapped[RebalanceResult] = relationship(
        "RebalanceResult", back_populates="items"
    )

    symbol_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Symbol.id), nullable=False
    )
    symbol: Mapped[Symbol] = relationship("Symbol")

    current_weight: Mapped[float] = mapped_column(Float, nullable=False)
    target_weight: Mapped[float] = mapped_column(Float, nullable=False)
    current_market_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_market_value: Mapped[float] = mapped_column(Float, nullable=False)
    delta_market_value: Mapped[float] = mapped_column(Float, nullable=False)

    def to_pydantic(self) -> PyRebalanceItem:
        return PyRebalanceItem(
            symbol=self.symbol.to_pydantic(),
            current_weight=float(self.current_weight),
            target_weight=float(self.target_weight),
            current_market_value=float(self.current_market_value),
            target_market_value=float(self.target_market_value),
            delta_market_value=float(self.delta_market_value),
        )

    @classmethod
    def from_pydantic(
        cls,
        item: PyRebalanceItem,
        symbol_id: int,
        result_id: int,
    ) -> Self:
        return cls(
            symbol_id=symbol_id,
            result_id=result_id,
            current_weight=item.current_weight,
            target_weight=item.target_weight,
            current_market_value=item.current_market_value,
            target_market_value=item.target_market_value,
            delta_market_value=item.delta_market_value,
        )
