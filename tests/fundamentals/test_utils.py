import pytest

from xarizmi.fundamentals.utils import (
    calculate_average_compound_return_rate_per_period,
)
from xarizmi.fundamentals.utils import calculate_compound_return_rate
from xarizmi.fundamentals.utils import calculate_return_rate_from_price


@pytest.mark.parametrize(
    ["old_price", "new_price", "expected_return_rate"],
    [(1, 1, 0), (1, 2, 1), (1, 0.5, -0.5), (0.3072, 237.33, 771)],
)
def test_calculate_return_rate_from_price(
    *, old_price: float, new_price: float, expected_return_rate: float
) -> None:
    assert calculate_return_rate_from_price(
        old_price=old_price,
        new_price=new_price,
    ) == pytest.approx(expected_return_rate, rel=0.001)


@pytest.mark.parametrize(
    ["n_periods", "return_rate_per_period", "expected_return_rate"],
    [
        (1, 0, 0),
        (1, 0.01, 0.01),
        (1, 0.1, 0.1),
        (2, 0.2, 0.44),
        (25, 0.07, 4.427),
        (25, 0.04, 1.6658),
    ],
)
def test_calculate_compound_return_rate(
    *,
    n_periods: int,
    return_rate_per_period: float,
    expected_return_rate: float
) -> None:
    assert calculate_compound_return_rate(
        n_periods=n_periods, return_rate_per_period=return_rate_per_period
    ) == pytest.approx(expected_return_rate, rel=0.0001)


@pytest.mark.parametrize(
    ["n_periods", "total_return_rate", "expected_return_rate"],
    [
        (1, 0, 0),
        (1, 0.01, 0.01),
        (1, 0.1, 0.1),
        (2, 0.44, 0.2),
        (25, 4.427, 0.07),
        (25, 1.6658, 0.04),
    ],
)
def test_calculate_average_compound_return_rate_per_period(
    *, n_periods: int, total_return_rate: float, expected_return_rate: float
) -> None:
    assert calculate_average_compound_return_rate_per_period(
        n_periods=n_periods, total_return_rate=total_return_rate
    ) == pytest.approx(expected_return_rate, rel=0.0001)
