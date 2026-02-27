from typing import Self

from sqlalchemy import Column, String

from xarizmi.db.models.base import Base
from xarizmi.models.currency import Currency as PyCurrency

from .constants import TableNamesEnum


class Currency(Base):  # type: ignore
    __tablename__ = TableNamesEnum.CURRENCY.value
    name = Column(String, primary_key=True, unique=True)

    def to_pydantic(self) -> PyCurrency:
        return PyCurrency(name=str(self.name))

    @classmethod
    def from_pydantic(cls, currency: PyCurrency) -> Self:
        return cls(name=currency.name)
