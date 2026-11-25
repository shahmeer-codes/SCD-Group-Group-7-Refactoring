import unittest

from model_objects import Product, ProductUnit, SpecialOfferType
from offer_strategies import (
    OFFER_STRATEGIES,
    BundleForAmountStrategy,
    PercentDiscountStrategy,
    ThreeForTwoStrategy,
)


class OfferStrategiesTest(unittest.TestCase):
    def setUp(self):
        self.toothbrush = Product("toothbrush", ProductUnit.EACH)
        self.apples = Product("apples", ProductUnit.KILO)

    def test_three_for_two_strategy(self):
        strategy = ThreeForTwoStrategy()
        self.assertIsNone(strategy.calculate_discount(self.toothbrush, 2, 0.99, 0.99))
        discount = strategy.calculate_discount(self.toothbrush, 3, 0.99, 0.99)
        self.assertEqual(discount.description, "3 for 2")
        self.assertAlmostEqual(discount.discount_amount, -0.99, places=2)

    def test_percent_discount_strategy(self):
        strategy = PercentDiscountStrategy()
        discount = strategy.calculate_discount(self.apples, 2.0, 1.99, 15.0)
        self.assertEqual(discount.description, "15.0% off")
        self.assertAlmostEqual(discount.discount_amount, -(2.0 * 1.99 * 0.15), places=4)

    def test_bundle_for_amount_strategy_five_for_amount(self):
        strategy = BundleForAmountStrategy(5, floor_bundle_count=True)
        self.assertIsNone(strategy.calculate_discount(self.apples, 4, 1.99, 5.99))
        discount = strategy.calculate_discount(self.apples, 6, 1.99, 5.99)
        self.assertEqual(discount.description, "5 for 5.99")
        expected = -(6 * 1.99 - (5.99 + 1.99))
        self.assertAlmostEqual(discount.discount_amount, expected, places=4)

    def test_all_offer_types_registered(self):
        for offer_type in SpecialOfferType:
            self.assertIn(offer_type, OFFER_STRATEGIES)
