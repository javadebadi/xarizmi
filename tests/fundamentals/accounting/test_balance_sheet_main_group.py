from unittest import TestCase

from xarizmi.fundamentals.accounting.balance_sheet_main_group import ASSET
from xarizmi.fundamentals.accounting.balance_sheet_main_group import (
    BALANCE_SHEET_MAIN_GROUP_OBJECTS,
)
from xarizmi.fundamentals.accounting.balance_sheet_main_group import EQUITY
from xarizmi.fundamentals.accounting.balance_sheet_main_group import LIABILITY
from xarizmi.fundamentals.accounting.balance_sheet_main_group import (
    BalanceSheetMainGroup,
)
from xarizmi.fundamentals.accounting.balance_sheet_main_group import (
    BalanceSheetMainGroupObjects,
)


class BalanceSheetMainGroupTest(TestCase):

    def test_balance_sheet_main_group(self) -> None:
        b = BalanceSheetMainGroup(id=1, name="Asset")
        self.assertEqual(b.name, "Asset")
        self.assertEqual(b.id, 1)
        self.assertEqual(b.to_csv(1), "1,Asset")
        self.assertEqual(b.to_csv(0), "1,Asset")
        self.assertEqual(b.to_csv(-1), "")


class BalanceSheetMainGroupObjectsIndividualTest(TestCase):

    def test_object_ASSET(self) -> None:
        self.assertEqual(ASSET.id, 1)
        self.assertEqual(ASSET.name, "Asset")

    def test_object_LIABILITY(self) -> None:
        self.assertEqual(LIABILITY.id, 2)
        self.assertEqual(LIABILITY.name, "Liability")

    def test_object_EQUITY(self) -> None:
        self.assertEqual(EQUITY.id, 3)
        self.assertEqual(EQUITY.name, "Equity")

    def test_object_BALANCE_SHEET_MAIN_GROUP_OBJECTS(self) -> None:
        self.assertEqual(BALANCE_SHEET_MAIN_GROUP_OBJECTS[0], ASSET)
        self.assertEqual(BALANCE_SHEET_MAIN_GROUP_OBJECTS[1], LIABILITY)
        self.assertEqual(BALANCE_SHEET_MAIN_GROUP_OBJECTS[2], EQUITY)


class BalanceSheetMainGroupObjectsTest(TestCase):

    def test_attribute_ASSET(self) -> None:
        self.assertIs(BalanceSheetMainGroupObjects.ASSET, ASSET)

    def test_attribute_LIABILITY(self) -> None:
        self.assertIs(BalanceSheetMainGroupObjects.LIABILITY, LIABILITY)

    def test_attribute_EQUITY(self) -> None:
        self.assertIs(BalanceSheetMainGroupObjects.EQUITY, EQUITY)
