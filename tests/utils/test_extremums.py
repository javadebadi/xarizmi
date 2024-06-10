import pytest

from xarizmi.utils.extremums import find_local_maxima_indexes
from xarizmi.utils.extremums import find_local_maxima_values
from xarizmi.utils.extremums import find_local_minima_indexes
from xarizmi.utils.extremums import find_local_minima_values


@pytest.mark.parametrize(
    "arr,expected_indexes",
    [
        ([0], [0]),
        ([100, 0], [1]),
        ([100, 50, 0], [2]),
        ([100, 50, 0, 50], [2]),
        ([100, 50, 0, 50, 100], [2]),
        ([100, 50, 0, 50, 100, 200], [2]),
        ([100, 50, 0, 50, 100, 200, 150], [2, 6]),
        ([100, 50, 0, 50, 100, 200, 150, 300], [2, 6]),
        ([100, 50, 0, 50, 100, 200, 150, 300, 300], [2, 6, 8]),
        ([100, 50, 0, 50, 100, 200, 150, 300, 300, 300], [2, 6, 8, 9]),
    ],
)
def test_find_local_minima_indexes(
    arr: list[int | float], expected_indexes: list[int]
) -> None:
    assert find_local_minima_indexes(arr) == expected_indexes


@pytest.mark.parametrize(
    "arr,expected_values",
    [
        ([0], [0]),
        ([100, 0], [0]),
        ([100, 50, 0], [0]),
        ([100, 50, 0, 50], [0]),
        ([100, 50, 0, 50, 100], [0]),
        ([100, 50, 0, 50, 100, 200], [0]),
        ([100, 50, 0, 50, 100, 200, 150], [0, 150]),
        ([100, 50, 0, 50, 100, 200, 150, 300], [0, 150]),
        ([100, 50, 0, 50, 100, 200, 150, 300, 300], [0, 150, 300]),
        ([100, 50, 0, 50, 100, 200, 150, 300, 300, 300], [0, 150, 300, 300]),
    ],
)
def test_find_local_minima_values(
    arr: list[int | float], expected_values: list[int]
) -> None:
    assert find_local_minima_values(arr) == expected_values


@pytest.mark.parametrize(
    "arr,expected_indexes",
    [
        ([0], [0]),
        ([100, 0], [0]),
        ([100, 50, 0], [0]),
        ([100, 50, 0, 50], [0, 3]),
        ([100, 50, 0, 50, 100], [0, 4]),
        ([100, 50, 0, 50, 100, 200], [0, 5]),
        ([100, 50, 0, 50, 100, 200, 150], [0, 5]),
        ([100, 50, 0, 50, 100, 200, 150, 300], [0, 5, 7]),
        ([100, 50, 0, 50, 100, 200, 150, 300, 300], [0, 5, 7, 8]),
    ],
)
def test_find_local_maxima_indexes(
    arr: list[int | float], expected_indexes: list[int]
) -> None:
    assert find_local_maxima_indexes(arr) == expected_indexes


@pytest.mark.parametrize(
    "arr,expected_indexes",
    [
        ([0], [0]),
        ([100, 0], [100]),
        ([100, 50, 0], [100]),
        ([100, 50, 0, 50], [100, 50]),
        ([100, 50, 0, 50, 100], [100, 100]),
        ([100, 50, 0, 50, 100, 200], [100, 200]),
        ([100, 50, 0, 50, 100, 200, 150], [100, 200]),
        ([100, 50, 0, 50, 100, 200, 150, 300], [100, 200, 300]),
        ([100, 50, 0, 50, 100, 200, 150, 300, 300], [100, 200, 300, 300]),
    ],
)
def test_find_local_maxima_values(
    arr: list[int | float], expected_indexes: list[int]
) -> None:
    assert find_local_maxima_values(arr) == expected_indexes
