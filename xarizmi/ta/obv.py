import matplotlib.pyplot as plt
import numpy as np
from talib import abstract

from xarizmi.candlestick import CandlestickChart


class OBVIndicator:

    def __init__(
        self, candlestick_chart: CandlestickChart, volume: str = "volume"
    ) -> None:
        self.candlestick_chart = candlestick_chart
        self.volume = volume
        self.indicator_data: None | list[float] = None

    def compute(self) -> list[float]:
        close = np.array(
            [candle.close for candle in self.candlestick_chart.candles]
        ).astype(np.float64)
        if self.volume == "volume":
            volume = np.array(
                [candle.volume for candle in self.candlestick_chart.candles]
            ).astype(np.float64)
        elif self.volume == "amount":
            volume = np.array(
                [candle.amount for candle in self.candlestick_chart.candles]
            ).astype(np.float64)
        self.indicator_data = abstract.OBV(close, volume)
        return self.indicator_data.tolist()  # type: ignore

    def plot(
        self,
        fig_size: tuple[int, int] = (10, 6),
        save_path: str | None = None,
        color: str = "blue",
    ) -> None:
        if self.indicator_data is None:
            raise RuntimeError("No data to plot")
        plt.figure(figsize=fig_size)
        dates = [candle.datetime for candle in self.candlestick_chart.candles]
        if any(value is None for value in dates):
            plt.plot(self.indicator_data, label="OBV", color=color)
        else:
            plt.plot(
                dates,  # type: ignore
                self.indicator_data,
                label="OBV",
                color=color,
            )
        plt.title("On-Balance Volume (OBV)")
        plt.xlabel("Time")
        plt.ylabel("OBV")
        plt.legend()
        plt.grid(True)

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
