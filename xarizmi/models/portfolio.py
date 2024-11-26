import datetime

from pydantic import BaseModel

from .symbol import Symbol


class PortfolioItem(BaseModel):
    symbol: Symbol
    market_value: float
    quantity: float
    datetime: datetime.datetime


class Portfolio(BaseModel):
    items: list[PortfolioItem]
