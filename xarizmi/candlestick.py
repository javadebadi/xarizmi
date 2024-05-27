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

    @property
    def range(self) -> float:
        """Range = H - L"""
        return self.high - self.low

    @property
    def intrinsic_range(self) -> float:
        """
        IR = R / L
        """
        if (self.low) == 0:
            return 0
        else:
            return self.range / (self.low)

    @property
    def body(self) -> float:
        """B = O - C"""
        return abs(self.open - self.close)

    @property
    def intrinsic_body(self) -> float:
        """B / R"""
        if self.range == 0:
            return 0
        return self.body / self.range


class CandlestickChart(BaseModel):
    candles: list[Candlestick]
