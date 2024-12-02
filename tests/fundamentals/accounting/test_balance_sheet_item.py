from unittest import TestCase

from xarizmi.fundamentals.accounting.balance_sheet_item import BalanceSheetItem
from xarizmi.fundamentals.accounting.balance_sheet_main_group import (
    BalanceSheetMainGroupObjects as BSMain,
)
from xarizmi.fundamentals.accounting.balance_sheet_submain_group import (
    BalanceSheetSubMainGroupObjects as BSSubMain,
)


class BalanceSheetItemTest(TestCase):

    def setUp(self) -> None:
        self.cash = BalanceSheetItem(
            ID="101-00000001",
            name="Cash",
            origin="Cash and Cash Equivalent",
            balance_sheet_sub_main_group=BSSubMain.SHORT_TERM_ASSET,
        )

    def test_balance_sheet_sub_main_group(self) -> None:
        b = BalanceSheetItem(
            ID="101-00000001",
            name="Cash",
            origin="Cash and Cash Equivalent",
            balance_sheet_sub_main_group=BSSubMain.SHORT_TERM_ASSET,
        )
        self.assertEqual(b.ID, "101-00000001")
        self.assertEqual(b.name, "Cash")
        self.assertEqual(b.origin, "Cash and Cash Equivalent")
        self.assertIs(
            b.bssubmain,
            BSSubMain.SHORT_TERM_ASSET,
        )
        self.assertIs(
            b.bsmain,
            BSMain.ASSET,
        )

    def test_is_main_asset(self) -> None:
        self.assertIs(self.cash.is_main_asset(), True)

    def test_is_main_liability(self) -> None:
        self.assertIs(self.cash.is_main_liability(), False)

    def test_is_main_equity(self) -> None:
        self.assertIs(self.cash.is_main_equity(), False)

    def test_is_short_term_asset(self) -> None:
        self.assertIs(self.cash.is_short_term_asset(), True)

    def test_is_long_term_asset(self) -> None:
        self.assertIs(self.cash.is_long_term_asset(), False)

    def test_is_short_term_liability(self) -> None:
        self.assertIs(self.cash.is_short_term_liability(), False)

    def test_is_long_term_liability(self) -> None:
        self.assertIs(self.cash.is_long_term_liability(), False)

    def test_is_equity(self) -> None:
        self.assertIs(self.cash.is_equity(), False)

    def test_to_csv(self) -> None:
        self.assertEqual(
            self.cash.to_csv(depth=2, end=""),
            "101-00000001,Cash,Cash and Cash Equivalent,1,"
            "Short Term Asset,1,Asset",
        )
        self.assertEqual(
            self.cash.to_csv(depth=1, end=""),
            "101-00000001,Cash,Cash and Cash Equivalent," "1,Short Term Asset",
        )
        self.assertEqual(
            self.cash.to_csv(depth=0, end=""),
            "101-00000001,Cash,Cash and Cash Equivalent",
        )
        self.assertEqual(self.cash.to_csv(depth=-1, end=""), "")
