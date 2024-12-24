import pytest

from xarizmi.fundamentals.time_value_money import time_value_money


class TestTimeValueMoney:

    @pytest.mark.parametrize(
        [
            "impatience_to_consume",
            "inflation",
            "risk",
            "expected_time_value_money",
        ],
        [
            pytest.param(0.01, 0, 0, 0.01, id="impatience_to_consume"),
            pytest.param(
                0.02, 0.03, 0, 0.0506, id="impatience_to_consume + inflation"
            ),
            pytest.param(
                0.02,
                0.03,
                0.05,
                0.1031,
                id="impatience_to_consume + inflation + risk",
            ),
            pytest.param(
                0.05,
                0.10,
                0.045,
                2069,
                id="impatience_to_consume + inflation + risk - xarizmi example",  # noqa: E501
            ),
        ],
    )
    def test_time_value_money(
        self,
        impatience_to_consume: float,
        inflation: float,
        risk: float,
        expected_time_value_money: float,
    ) -> None:
        assert time_value_money(
            impatience_to_consume=impatience_to_consume,
            inflation=inflation,
            risk=risk,
        ) == pytest.approx(expected_time_value_money, rel=0.001)
