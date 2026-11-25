import unittest

from catalog import SupermarketCatalog
from model_objects import Discount, Product, ProductUnit, SpecialOfferType
from receipt import Receipt
from receipt_printer import ReceiptPrinter
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


class CharacterizationTest(unittest.TestCase):
    def setUp(self):
        self.catalog = FakeCatalog()
        self.teller = Teller(self.catalog)
        self.cart = ShoppingCart()

        self.toothbrush = Product("toothbrush", ProductUnit.EACH)
        self.catalog.add_product(self.toothbrush, 0.99)

        self.apples = Product("apples", ProductUnit.KILO)
        self.catalog.add_product(self.apples, 1.99)

        self.rice = Product("rice", ProductUnit.EACH)
        self.catalog.add_product(self.rice, 2.49)

        self.cherry_tomatoes = Product("cherry tomato box", ProductUnit.EACH)
        self.catalog.add_product(self.cherry_tomatoes, 0.69)

    def test_three_for_two_below_threshold_gives_no_discount(self):
        self.teller.add_special_offer(
            SpecialOfferType.THREE_FOR_TWO, self.toothbrush, 0.99
        )
        self.cart.add_item_quantity(self.toothbrush, 2)

        receipt = self.teller.checks_out_articles_from(self.cart)

        self.assertEqual(len(receipt.discounts), 0)
        self.assertAlmostEqual(receipt.total_price(), 1.98, places=2)

    def test_three_for_two_for_six_items_applies_twice(self):
        self.teller.add_special_offer(
            SpecialOfferType.THREE_FOR_TWO, self.toothbrush, 0.99
        )
        self.cart.add_item_quantity(self.toothbrush, 6)

        receipt = self.teller.checks_out_articles_from(self.cart)

        self.assertEqual(len(receipt.discounts), 1)
        self.assertEqual(receipt.discounts[0].description, "3 for 2")
        self.assertAlmostEqual(receipt.discounts[0].discount_amount, -1.98, places=2)
        self.assertAlmostEqual(receipt.total_price(), 3.96, places=2)

    def test_two_for_amount_below_threshold_gives_no_discount(self):
        self.teller.add_special_offer(
            SpecialOfferType.TWO_FOR_AMOUNT, self.cherry_tomatoes, 0.99
        )
        self.cart.add_item(self.cherry_tomatoes)

        receipt = self.teller.checks_out_articles_from(self.cart)

        self.assertEqual(len(receipt.discounts), 0)
        self.assertAlmostEqual(receipt.total_price(), 0.69, places=2)

    def test_two_for_amount_with_three_items_preserves_existing_calculation(self):
        # Captures current behavior: total = argument * (3 / 2) + (3 % 2) * unit_price
        self.teller.add_special_offer(
            SpecialOfferType.TWO_FOR_AMOUNT, self.cherry_tomatoes, 0.99
        )
        self.cart.add_item_quantity(self.cherry_tomatoes, 3)

        receipt = self.teller.checks_out_articles_from(self.cart)

        self.assertEqual(len(receipt.discounts), 1)
        self.assertEqual(receipt.discounts[0].description, "2 for 0.99")
        expected_total = 0.99 * (3 / 2) + 0.69
        self.assertAlmostEqual(receipt.total_price(), expected_total, places=4)

    def test_percent_discount_on_loose_weight_product(self):
        self.teller.add_special_offer(
            SpecialOfferType.TEN_PERCENT_DISCOUNT, self.apples, 20.0
        )
        self.cart.add_item_quantity(self.apples, 2.5)

        receipt = self.teller.checks_out_articles_from(self.cart)

        self.assertEqual(len(receipt.discounts), 1)
        self.assertEqual(receipt.discounts[0].description, "20.0% off")
        expected_discount = -(2.5 * 1.99 * 20.0 / 100.0)
        self.assertAlmostEqual(
            receipt.discounts[0].discount_amount, expected_discount, places=4
        )
        self.assertAlmostEqual(
            receipt.total_price(), 2.5 * 1.99 + expected_discount, places=4
        )

    def test_multiple_add_item_calls_aggregate_for_offer_but_keep_receipt_lines(self):
        self.teller.add_special_offer(
            SpecialOfferType.THREE_FOR_TWO, self.toothbrush, 0.99
        )
        self.cart.add_item(self.toothbrush)
        self.cart.add_item_quantity(self.toothbrush, 2)

        receipt = self.teller.checks_out_articles_from(self.cart)

        self.assertEqual(len(receipt.items), 2)
        self.assertEqual(len(receipt.discounts), 1)
        self.assertAlmostEqual(receipt.total_price(), 1.98, places=2)

    def test_teller_product_with_name_found_and_missing(self):
        self.assertIs(self.teller.product_with_name("rice"), self.rice)
        self.assertIsNone(self.teller.product_with_name("milk"))

    def test_receipt_returns_defensive_copies(self):
        receipt = Receipt()
        receipt.add_product(self.rice, 1, 2.49, 2.49)
        receipt.add_discount(Discount(self.rice, "10% off", -0.25))

        items_copy = receipt.items
        discounts_copy = receipt.discounts
        items_copy.clear()
        discounts_copy.clear()

        self.assertEqual(len(receipt.items), 1)
        self.assertEqual(len(receipt.discounts), 1)
        self.assertAlmostEqual(receipt.total_price(), 2.24, places=2)

    def test_receipt_printer_custom_columns_and_each_quantity_formatting(self):
        receipt = Receipt()
        receipt.add_product(self.toothbrush, 2, 0.99, 1.98)

        output = ReceiptPrinter(columns=30).print_receipt(receipt)
        lines = output.splitlines()

        self.assertEqual(len(lines[0]), 30)
        self.assertEqual(lines[1], "  0.99 * 2")
        self.assertEqual(len(lines[3]), 30)

    def test_base_supermarket_catalog_raises_exception(self):
        catalog = SupermarketCatalog()
        with self.assertRaises(Exception):
            catalog.add_product(self.toothbrush, 0.99)
        with self.assertRaises(Exception):
            catalog.unit_price(self.toothbrush)
