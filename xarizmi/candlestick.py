from datetime import datetime as dt

from pydantic import BaseModel
from pydantic import NonNegativeFloat

from xarizmi.config import config
from xarizmi.enums import IntervalTypeEnum
from xarizmi.models.symbol import Symbol
from xarizmi.utils.extremums import find_local_minima_values
from xarizmi.utils.numbers import round_to_significant_digit


class Candlestick(BaseModel):
    """This class contains basic properties of a candlestick.

    :param close: the closing price for the corresponding time period
    :type close: float
    :param open: the opening price for the corresponding time period
    :type open: float
    :param low: the lowest traded price for the corresponding time period
    :type low: float
    :param high: the highest traded price for the corresponding time period
    :type high: float
    :param volume: the amount of trading volume (width of the candlestick)
    :type volume: float
    :param amount: [amount description?]
    :type amount: float
    :param interval_type: the time period for each candlestick
    :type interval_type: str
    :param symbol: the type of the trade, e.g., "CAD-USD" or "BTC-USDT"
    :type symbol: str
    """

    close: NonNegativeFloat
    open: NonNegativeFloat
    low: NonNegativeFloat
    high: NonNegativeFloat
    volume: NonNegativeFloat
    amount: NonNegativeFloat | None = None
    interval_type: IntervalTypeEnum | None = None
    interval: int | None = None  # interval in seconds
    symbol: Symbol | None = None
    datetime: dt | None = None

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

    def get_local_minimas(
        self, price_type: str = "low", only_significant_digit: bool = False
    ) -> list[int | float]:
        if price_type not in ["low", "high", "close", "open"]:
            raise ValueError(
                "The given value for price_type ="
                f" '{price_type}' is not valid!"
            )
        values = find_local_minima_values(
            [getattr(candle, price_type) for candle in self.candles]
        )
        if only_significant_digit is True:
            values = [round_to_significant_digit(item) for item in values]
        return values
