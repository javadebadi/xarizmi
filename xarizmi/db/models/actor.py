from typing import Self

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from xarizmi.db.models.base import Base
from xarizmi.models.actors import Actor as PyActor
from xarizmi.models.actors import ExchangeActor as PyExchangeActor
from xarizmi.models.actors import InvestorActor as PyInvestorActor
from xarizmi.models.actors import TraderActor as PyTraderActor

from .constants import TableNamesEnum


class Actor(Base):  # type: ignore
    __tablename__ = TableNamesEnum.ACTOR.value
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    actor_type: Mapped[str] = mapped_column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_on": "actor_type",
        "polymorphic_identity": "actor",
    }

    def to_pydantic(self) -> PyActor:
        return PyActor(asset=float(self.asset))

    @classmethod
    def from_pydantic(cls, actor: PyActor) -> Self:
        return cls(asset=actor.asset)


class ExchangeActor(Actor):  # type: ignore
    __mapper_args__ = {"polymorphic_identity": "exchange_actor"}

    def to_pydantic(self) -> PyExchangeActor:  # type: ignore[override]
        return PyExchangeActor(asset=float(self.asset))

    @classmethod
    def from_pydantic(cls, actor: PyExchangeActor) -> Self:  # type: ignore[override]
        return cls(asset=actor.asset)


class TraderActor(Actor):  # type: ignore
    __mapper_args__ = {"polymorphic_identity": "trader_actor"}

    def to_pydantic(self) -> PyTraderActor:  # type: ignore[override]
        return PyTraderActor(asset=float(self.asset))

    @classmethod
    def from_pydantic(cls, actor: PyTraderActor) -> Self:  # type: ignore[override]
        return cls(asset=actor.asset)


class InvestorActor(Actor):  # type: ignore
    __mapper_args__ = {"polymorphic_identity": "investor_actor"}

    def to_pydantic(self) -> PyInvestorActor:  # type: ignore[override]
        return PyInvestorActor(asset=float(self.asset))

    @classmethod
    def from_pydantic(cls, actor: PyInvestorActor) -> Self:  # type: ignore[override]
        return cls(asset=actor.asset)
