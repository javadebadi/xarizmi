import numpy as np
from talib import abstract

from xarizmi.candlestick import CandlestickChart
from xarizmi.utils.plot.timeseries.lineplot import lineplot_timeseries


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
        lineplot_timeseries(
            data=self.indicator_data,
            dates_data=[
                candle.datetime for candle in self.candlestick_chart.candles
            ],
            fig_size=fig_size,
            save_path=save_path,
            color=color,
            label="OBV",
            xlabel="Time",
            ylabel="OBV",
            title="On-Balance Volume (OBV)",
        )
