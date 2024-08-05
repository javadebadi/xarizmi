from typing import Any
from numpy import ndarray, dtype, float64
import numpy.typing as npt
import numpy as np


def OBV(
    close: list[float] | ndarray[Any, dtype[float64]],
    volume: list[float] | ndarray[Any, dtype[float64]],
) -> npt.NDArray[np.float64]: ...
