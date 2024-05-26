import pytest
from pydantic import ValidationError

from xarizmi.candlestick import Candlestick
from xarizmi.candlestick import CandlestickChart


class TestCandlestick:
    def test(self) -> None:
        data = {
            "close": 2.5,
            "open": 1,
            "low": 0.5,
            "high": 3,
            "volume": 100,
            "amount": 150,
        }
        candle = Candlestick(**data)
        assert candle.close == 2.5
        assert candle.open == 1
        assert candle.low == 0.5
        assert candle.high == 3
        assert candle.range == 2.5

        assert candle.model_dump() == pytest.approx(
            {
                "close": 2.5,
                "open": 1,
                "low": 0.5,
                "high": 3,
                "interval_type": None,
                "interval": None,
                "symbol": None,
                "volume": 100,
                "amount": 150,
            }
        )

    def test_intrinsic_rang(self) -> None:
        zero_data = {
            "close": 0,
            "open": 0,
            "low": 0,
            "high": 0,
            "volume": 0,
            "amount": 0,
        }
        candle = Candlestick(**zero_data)
        assert candle.intrinsic_range == 0
        data = {
            "close": 2.5,
            "open": 1,
            "low": 0.5,
            "high": 3,
            "volume": 100,
            "amount": 150,
        }
        candle = Candlestick(**data)
        assert candle.intrinsic_range == 2.5 / 3.5

    def test_negative_price(self) -> None:
        # Given a data with negative price
        data = {
            "close": -2.5,
            "open": 1,
            "low": 0.5,
            "high": 3,
            "volume": 100,
            "amount": 150,
        }
        # When Candlestick constructor is called
        # Then I should see ValidationError
        with pytest.raises(ValidationError):
            Candlestick(**data)


class TestCandlestickChart:

    def test(self) -> None:
        data = {
            "candles": [
                {
                    "low": 0.61873,
                    "high": 0.727,
                    "close": 0.714,
                    "open": 0.71075,
                    "interval_type": "1week",
                    "interval": 604800,
                    "symbol": None,
                    "volume": 100,
                    "amount": 150,
                },
                {
                    "low": 0.65219,
                    "high": 0.75,
                    "close": 0.70238,
                    "open": 0.71075,
                    "interval_type": "1week",
                    "interval": 604800,
                    "symbol": None,
                    "volume": 100,
                    "amount": 150,
                },
                {
                    "low": 0.64801,
                    "high": 0.92,
                    "close": 0.8404,
                    "open": 0.70238,
                    "interval_type": "1week",
                    "interval": 604800,
                    "symbol": None,
                    "volume": 100,
                    "amount": 150,
                },
            ]
        }

        chart = CandlestickChart(**data)

        assert chart.model_dump() == pytest.approx(data)
