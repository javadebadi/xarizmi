from pydantic import BaseModel
from pydantic import NonNegativeFloat

from xarizmi.config import config
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
    def is_bullish(self) -> bool:
        if self.close >= self.open:
            return True
        else:
            return False

    @property
    def is_bearish(self) -> bool:
        if self.open >= self.close:
            return True
        else:
            return False

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

    @property
    def upper_shadow(self) -> float:
        """US = H - MAX(C, O)"""
        return self.high - max(self.close, self.open)

    @property
    def intrinsic_upper_shadow(self) -> float:
        """US / R"""
        if self.range == 0:
            return 0
        return self.upper_shadow / self.range

    @property
    def lower_shadow(self) -> float:
        """LS = min(C, O) - L"""
        return min(self.close, self.open) - self.low

    @property
    def intrinsic_lower_shadow(self) -> float:
        """LS / R"""
        if self.range == 0:
            return 0
        return self.lower_shadow / self.range

    @property
    def doginess(self) -> float:
        if self.range == 0:
            return 0
        return 1 - self.intrinsic_body

    @property
    def is_doji(self) -> bool:
        if self.range == 0:
            return False
        return self.doginess >= config.DOJINESS_THRESHOLD


class CandlestickChart(BaseModel):
    candles: list[Candlestick]
