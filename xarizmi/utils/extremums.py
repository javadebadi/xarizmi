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
    return argrelextrema(np.array(arr), np.less_equal)[0].tolist()  # type: ignore  # noqa: E501


def find_local_minima_values(arr: list[int | float]) -> list[int | float]:
    """
    Finds the values of local minima values in a list using scipy.

    Parameters:
    arr (list of int/float): The list of values to find local minima in.

    Returns:
    list of int/float: Values of local minima.
    """
    return [arr[i] for i in find_local_minima_indexes(arr)]


def find_local_maxima_indexes(arr: list[int | float]) -> list[int]:
    """
    Finds the indices of local maxima indexes in a list using scipy.

    Parameters:
    arr (list of int/float): The list of values to find local maxima in.

    Returns:
    list of int: Indices of local maxima.
    """
    return argrelextrema(np.array(arr), np.greater_equal)[0].tolist()  # type: ignore  # noqa: E501


def find_local_maxima_values(arr: list[int | float]) -> list[int | float]:
    """
    Finds the values of local maxima values in a list using scipy.

    Parameters:
    arr (list of int/float): The list of values to find local maxima in.

    Returns:
    list of int/float: Values of local maxima.
    """
    return [arr[i] for i in find_local_maxima_indexes(arr)]
