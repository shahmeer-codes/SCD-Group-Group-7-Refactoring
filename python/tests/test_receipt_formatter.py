import unittest

from model_objects import Discount, Product, ProductUnit
from receipt import ReceiptItem
from receipt_printer import ReceiptFormatter, ReceiptPrinter


class ReceiptFormatterTest(unittest.TestCase):
    def setUp(self):
        self.formatter = ReceiptFormatter()
        self.toothbrush = Product("toothbrush", ProductUnit.EACH)
        self.apples = Product("apples", ProductUnit.KILO)

    def test_format_price(self):
        self.assertEqual(self.formatter.format_price(0.99), "0.99")
        self.assertEqual(self.formatter.format_price(-1.5), "-1.50")

    def test_format_quantity_each_and_kilo(self):
        each_item = ReceiptItem(self.toothbrush, 2, 0.99, 1.98)
        kilo_item = ReceiptItem(self.apples, 1.25, 1.99, 2.4875)
        self.assertEqual(self.formatter.format_quantity(each_item), "2")
        self.assertEqual(self.formatter.format_quantity(kilo_item), "1.250")

    def test_format_discount_label(self):
        discount = Discount(self.toothbrush, "3 for 2", -0.99)
        self.assertEqual(
            self.formatter.format_discount_label(discount),
            "3 for 2 (toothbrush)",
        )

    def test_default_columns_constant(self):
        self.assertEqual(ReceiptPrinter.DEFAULT_COLUMNS, 40)
        self.assertEqual(ReceiptPrinter().columns, 40)
