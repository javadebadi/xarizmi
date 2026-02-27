from typing import Self

from sqlalchemy import Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from xarizmi.db.models.base import Base
from xarizmi.enums import OrderStatusEnum, SideEnum
from xarizmi.models.orders import Order as PyOrder

from .constants import TableNamesEnum
from .symbol import Symbol


class Order(Base):  # type: ignore
    __tablename__ = TableNamesEnum.ORDER.value
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    symbol_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Symbol.id), nullable=False
    )
    symbol: Mapped[Symbol] = relationship("Symbol", back_populates="orders")

    order_id: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    side: Mapped[str] = mapped_column(
        Enum(SideEnum, name="side_enum", create_type=True),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        Enum(OrderStatusEnum, name="order_status_enum", create_type=True),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "symbol_id",
            "order_id",
            name="uix_symbol_id_order_id",
        ),
    )

    def to_pydantic(self) -> PyOrder:
        return PyOrder(
            symbol=self.symbol.to_pydantic(),
            price=float(self.price),
            amount=float(self.amount),
            status=OrderStatusEnum(self.status),
            side=SideEnum(self.side),
            order_id=str(self.order_id) if self.order_id else None,
        )

    @classmethod
    def from_pydantic(cls, order: PyOrder, symbol_id: int) -> Self:
        return cls(
            symbol_id=symbol_id,
            order_id=order.order_id or "",
            amount=order.amount,
            price=order.price,
            side=order.side,
            status=order.status,
        )
