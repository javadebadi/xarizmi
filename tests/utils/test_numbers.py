import pytest

from xarizmi.utils.numbers import round_to_significant_digit


@pytest.mark.parametrize(
    "number,expected_value",
    [
        (5800, 6000),
        (5300, 5000),
        (54390, 50000),
        (58900, 60000),
        (511, 500),
        (0.0134, 0.01),
        (0.0467, 0.05),
        (0.0081, 0.008),
        (1, 1),
        (9, 9),
        (10, 10),
        (0.9, 0.9),
        (0.49, 0.5),
        (0.41, 0.4),
        (0.99, 1),
        (0, 0),
    ],
)
def test_round_to_significant_digit(
    number: int | float, expected_value: int
) -> None:
    assert round_to_significant_digit(number) == expected_value
