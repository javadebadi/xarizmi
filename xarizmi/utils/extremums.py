import numpy as np
from scipy.signal import argrelextrema  # type: ignore


def find_local_minima_indexes(arr: list[int | float]) -> list[int]:
    """
    Finds the indices of local minima indexes in a list using scipy.

    Parameters:
    arr (list of int/float): The list of values to find local minima in.

    Returns:
    list of int: Indices of local minima.
    """
    # Convert the list to a numpy array
    arr = np.array(arr)  # type: ignore

    # Find indices of local minima
    return argrelextrema(arr, np.less)[0].tolist()  # type: ignore


def find_local_minima_values(arr: list[int | float]) -> list[int | float]:
    """
    Finds the values of local minima values in a list using scipy.

    Parameters:
    arr (list of int/float): The list of values to find local minima in.

    Returns:
    list of int/float: Values of local minima.
    """
    # Get indices of local minima
    local_minima_indices = find_local_minima_indexes(arr)

    # Retrieve the corresponding values
    local_minima_values = [arr[i] for i in local_minima_indices]

    return local_minima_values
