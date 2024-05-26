from pydantic import BaseModel
from pydantic import NonNegativeFloat

from xarizmi.enums import IntervalTypeEnum
from xarizmi.models.symbol import Symbol


class Candlestick(BaseModel):
    close: NonNegativeFloat
    open: NonNegativeFloat
    low: NonNegativeFloat
    high: NonNegativeFloat
    volume: NonNegativeFloat
    amount: NonNegativeFloat | None = None
    interval_type: IntervalTypeEnum | None = None
    interval: int | None = None  # interval in seconds
    symbol: Symbol | None = None


class CandlestickChart(BaseModel):
    candles: list[Candlestick]
