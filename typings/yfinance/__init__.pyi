from typing import Any
import pandas as pd

def download(
    tickers: str,
    start: str | None = None,
    end: str | None = None,
    actions: bool = False,
    threads: bool = True,
    ignore_tz: bool | None = None,
    group_by: str = "column",
    auto_adjust: bool = False,
    back_adjust: bool = False,
    repair: bool = False,
    keepna: bool = False,
    progress: bool = True,
    period: str = "max",
    interval: str = "1d",
    prepost: bool = False,
    proxy: str | None = None,
    rounding: bool = False,
    timeout: int | float = 10,
    session: Any | None = None,
) -> pd.DataFrame: ...
