import pytest

from xarizmi.fundamentals.fundamentals import Fundamentals


@pytest.fixture(scope="session")
def apple_finance_fundamentals_2024() -> dict[str, float | int]:
    return {
        "reported_earning": 6.08 * int(15.12e9),
        "number_of_shares": int(15.12e9),
        "share_price": 237.33,
        "enterprise_value": 3.64e12,
        "reported_earnings_before_interest_tax_depreciation_amortization": 3.64e12  # noqa: E501
        / 27.04,
        "cash_and_cash_equivalents": 65.17e9,
        "total_debt": 119e9,
    }


class TestFundamentals:

    def test(
        self, apple_finance_fundamentals_2024: dict[str, float | int]
    ) -> None:
        f = Fundamentals(
            reported_earnings=apple_finance_fundamentals_2024[
                "reported_earning"
            ],
            number_of_shares=apple_finance_fundamentals_2024[
                "number_of_shares"
            ],
            share_price=apple_finance_fundamentals_2024["share_price"],
            enterprise_value=apple_finance_fundamentals_2024[
                "enterprise_value"
            ],
            reported_earnings_before_interest_tax_depreciation_amortization=apple_finance_fundamentals_2024[  # noqa: E501
                "reported_earnings_before_interest_tax_depreciation_amortization"  # noqa: E501
            ],
            cash_and_cash_equivalents=apple_finance_fundamentals_2024[
                "cash_and_cash_equivalents"
            ],
            total_debt=apple_finance_fundamentals_2024["total_debt"],
        )

        assert (
            f.reported_earnings
            == apple_finance_fundamentals_2024["reported_earning"]
        )
        assert (
            f.number_of_shares
            == apple_finance_fundamentals_2024["number_of_shares"]
        )
        assert (
            f.enterprise_value
            == apple_finance_fundamentals_2024["enterprise_value"]
        )
        assert (
            f.reported_earnings_before_interest_tax_depreciation_amortization
            == apple_finance_fundamentals_2024[
                "reported_earnings_before_interest_tax_depreciation_amortization"  # noqa: E501
            ]
        )
        assert f.share_price == apple_finance_fundamentals_2024["share_price"]
        assert f.earnings_per_share == pytest.approx(6.08)
        assert f.EPS == pytest.approx(6.08)
        assert f.price_to_earnings_ratio == pytest.approx(39, rel=0.001)
        assert f.PE == pytest.approx(39, rel=0.001)
        assert (
            f.EBITDA
            == apple_finance_fundamentals_2024[
                "reported_earnings_before_interest_tax_depreciation_amortization"  # noqa: E501
            ]
        )
        assert f.enterprise_value_to_EBITDA_ratio == pytest.approx(
            27.04, rel=0.001
        )
        assert f.market_capitalization == pytest.approx(3.5884e12, rel=0.01)
        assert (
            f.cash_and_cash_equivalents
            == apple_finance_fundamentals_2024["cash_and_cash_equivalents"]
        )
        assert (
            f.enterprise_value
            - f.market_capitalization
            + f.cash_and_cash_equivalents
        ) == pytest.approx(f.total_debt, rel=0.1)
