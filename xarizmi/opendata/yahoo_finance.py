"""A client to download Yahoo Finance data
"""

from datetime import datetime

import pandas as pd
import yfinance as yf

from xarizmi.candlestick import CandlestickChart


class YahooFinanceDailyDataClient:

    def __init__(
        self,
        symbol: str,
        start_date: str = "1900-01-01",
        end_date: str | None = None,
    ) -> None:
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date

    def extract(self) -> list[dict[str, str | float | pd.Timestamp]] | None:
        stock_data: pd.DataFrame = yf.download(
            self.symbol, start=self.start_date, end=self.end_date
        )

        if stock_data.empty:
            print("Error fetching data for symbol:", self.symbol)
            return None

        # Reset the index to get 'Date' as a column
        stock_data.reset_index(inplace=True)

        return stock_data.to_dict(orient="records")  # type: ignore

    def transform(
        self, data_list: list[dict[str, str | float | pd.Timestamp]]
    ) -> list[dict[str, str | float | datetime | dict[str, dict[str, str]]]]:
        candles_data = []
        for single_candle_data in data_list:
            temp = {}
            temp["open"] = single_candle_data["Open"]
            temp["high"] = single_candle_data["High"]
            temp["low"] = single_candle_data["Low"]
            temp["close"] = single_candle_data["Close"]
            temp["volume"] = single_candle_data["Volume"]
            temp["datetime"] = single_candle_data["Date"].to_pydatetime()  # type: ignore  # noqa:E501
            temp["interval_type"] = "1day"
            temp["symbol"] = {
                "base_currency": {"name": self.symbol},
                "quote_currency": {"name": "CAD"},
                "fee_currency": {"name": "CAD"},
            }  # type: ignore
            candles_data.append(temp)
        return candles_data  # type: ignore

    def save_file(
        self,
        candles_data: list[
            dict[str, str | float | datetime | dict[str, dict[str, str]]]
        ],
        filepath: str,
        indent: int = 4,
    ) -> None:
        candles = CandlestickChart.model_validate({"candles": candles_data})
        with open(filepath, "w") as f:
            f.write(candles.model_dump_json(indent=indent))

    def etl(self, filepath: str) -> None:
        data_list = self.extract()
        if data_list:
            candles_data = self.transform(data_list=data_list)
            self.save_file(candles_data=candles_data, filepath=filepath)
