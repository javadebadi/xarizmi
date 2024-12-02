import unittest

from xarizmi.fundamentals.time_value_money import time_value_money


class TimeValueMoney(unittest.TestCase):

    def test_time_value_money(self) -> None:
        self.assertEqual(round(time_value_money(0.01, 0, 0), 2), 0.01)
        self.assertEqual(round(time_value_money(0.02, 0.03, 0), 4), 0.0506)
        self.assertEqual(round(time_value_money(0.02, 0.03, 0.05), 4), 0.1031)
