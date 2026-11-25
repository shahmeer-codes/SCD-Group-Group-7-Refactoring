import unittest

from model_objects import (
    Discount,
    Offer,
    Product,
    ProductQuantity,
    ProductUnit,
    SpecialOfferType,
)
from receipt import Receipt, ReceiptItem


class ReceiptAndDomainModelsTest(unittest.TestCase):
    def setUp(self):
        self.toothbrush = Product("toothbrush", ProductUnit.EACH)
        self.apples = Product("apples", ProductUnit.KILO)

    def test_receipt_items_total_and_discounts_total(self):
        receipt = Receipt()
        receipt.add_product(self.toothbrush, 3, 0.99, 2.97)
        receipt.add_product(self.apples, 1.0, 1.99, 1.99)
        receipt.add_discount(Discount(self.toothbrush, "3 for 2", -0.99))

        self.assertAlmostEqual(receipt.items_total(), 4.96, places=2)
        self.assertAlmostEqual(receipt.discounts_total(), -0.99, places=2)
        self.assertAlmostEqual(receipt.total_price(), 3.97, places=2)

    def test_empty_receipt_totals_zero(self):
        receipt = Receipt()
        self.assertEqual(receipt.items_total(), 0)
        self.assertEqual(receipt.discounts_total(), 0)
        self.assertEqual(receipt.total_price(), 0)

    def test_domain_objects_repr_contains_key_fields(self):
        pq = ProductQuantity(self.toothbrush, 2)
        offer = Offer(SpecialOfferType.THREE_FOR_TWO, self.toothbrush, 0.99)
        discount = Discount(self.toothbrush, "3 for 2", -0.99)
        item = ReceiptItem(self.toothbrush, 2, 0.99, 1.98)

        self.assertIn("toothbrush", repr(self.toothbrush))
        self.assertIn("quantity=2", repr(pq))
        self.assertIn("THREE_FOR_TWO", repr(offer))
        self.assertIn("3 for 2", repr(discount))
        self.assertIn("total_price=1.98", repr(item))
