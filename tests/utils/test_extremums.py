import pytest

from xarizmi.utils.extremums import find_local_minima_indexes
from xarizmi.utils.extremums import find_local_minima_values


@pytest.mark.parametrize(
    "arr,expected_indexes",
    [
        ([0], []),
        ([100, 0], []),
        ([100, 50, 0], []),
        ([100, 50, 0, 50], [2]),
        ([100, 50, 0, 50, 100], [2]),
        ([100, 50, 0, 50, 100, 200], [2]),
        ([100, 50, 0, 50, 100, 200, 150], [2]),
        ([100, 50, 0, 50, 100, 200, 150, 300], [2, 6]),
    ],
)
def test_find_local_minima_indexes(
    arr: list[int | float], expected_indexes: list[int]
) -> None:
    assert find_local_minima_indexes(arr) == expected_indexes


@pytest.mark.parametrize(
    "arr,expected_values",
    [
        ([0], []),
        ([100, 0], []),
        ([100, 50, 0], []),
        ([100, 50, 0, 50], [0]),
        ([100, 50, 0, 50, 100], [0]),
        ([100, 50, 0, 50, 100, 200], [0]),
        ([100, 50, 0, 50, 100, 200, 150], [0]),
        ([100, 50, 0, 50, 100, 200, 150, 300], [0, 150]),
    ],
)
def test_find_local_minima_values(
    arr: list[int | float], expected_values: list[int]
) -> None:
    assert find_local_minima_values(arr) == expected_values
