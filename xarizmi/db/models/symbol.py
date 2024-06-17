from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.schema import Computed
from sqlalchemy.schema import UniqueConstraint

from xarizmi.db.models.base import Base


class Symbol(Base):  # type: ignore
    __tablename__ = "xarizmi_symbol"
    id = Column(Integer, primary_key=True)
    base_currency = Column(String, nullable=False)
    quote_currency = Column(String, nullable=False)
    fee_currency = Column(String, nullable=True)
    name = Column(
        String, Computed("base_currency || '-' || quote_currency"), unique=True
    )

    @property
    def symbol(self) -> str:
        return f"{self.base_currency}-{self.quote_currency}"

    __table_args__ = (
        UniqueConstraint(
            "base_currency", "quote_currency", name="uix_symbol_name"
        ),
    )
