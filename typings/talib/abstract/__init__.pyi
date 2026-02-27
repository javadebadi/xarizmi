from typing import Any

import numpy as np
import numpy.typing as npt
from numpy import dtype, float64, ndarray

def OBV(
    close: list[float] | ndarray[Any, dtype[float64]],
    volume: list[float] | ndarray[Any, dtype[float64]],
) -> npt.NDArray[np.float64]: ...
