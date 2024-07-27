from typing import Any
from numpy import ndarray, dtype, floating, float64

def OBV(close: list[float] | ndarray[Any, dtype[float64]], volume: list[float] | ndarray[Any, dtype[float64]]) -> list[float]: ...
