from abc import ABC, abstractmethod
import math

from model_objects import Discount, SpecialOfferType


class OfferStrategy(ABC):
    """Strategy interface for calculating a promotional discount on a product."""

    @abstractmethod
    def calculate_discount(self, product, quantity, unit_price, argument):
        """Return a Discount if the offer applies, or None otherwise."""


class ThreeForTwoStrategy(OfferStrategy):
    """Buy-three-for-the-price-of-two offer strategy."""

    BUNDLE_SIZE = 3
    PAID_ITEMS_PER_BUNDLE = 2

    def calculate_discount(self, product, quantity, unit_price, argument):
        quantity_as_int = int(quantity)
        if quantity_as_int < self.BUNDLE_SIZE:
            return None
        bundle_count = math.floor(quantity_as_int / self.BUNDLE_SIZE)
        remainder = quantity_as_int % self.BUNDLE_SIZE
        discounted_total = (
            bundle_count * self.PAID_ITEMS_PER_BUNDLE * unit_price
            + remainder * unit_price
        )
        discount_amount = quantity * unit_price - discounted_total
        return Discount(product, "3 for 2", -discount_amount)


class PercentDiscountStrategy(OfferStrategy):
    """Percentage-off offer strategy."""

    PERCENT_DIVISOR = 100.0

    def calculate_discount(self, product, quantity, unit_price, argument):
        discount_amount = quantity * unit_price * argument / self.PERCENT_DIVISOR
        return Discount(product, f"{argument}% off", -discount_amount)


class BundleForAmountStrategy(OfferStrategy):
    """Multi-buy fixed-bundle-price offer strategy (e.g., 2-for-X, 5-for-X)."""

    def __init__(self, bundle_size, floor_bundle_count=True):
        self.bundle_size = bundle_size
        self.floor_bundle_count = floor_bundle_count

    def calculate_discount(self, product, quantity, unit_price, argument):
        quantity_as_int = int(quantity)
        if quantity_as_int < self.bundle_size:
            return None
        if self.floor_bundle_count:
            bundle_count = math.floor(quantity_as_int / self.bundle_size)
        else:
            # Preserves legacy float division behavior for TWO_FOR_AMOUNT.
            bundle_count = quantity_as_int / self.bundle_size
        remainder = quantity_as_int % self.bundle_size
        discounted_total = argument * bundle_count + remainder * unit_price
        discount_amount = unit_price * quantity - discounted_total
        return Discount(product, f"{self.bundle_size} for {argument}", -discount_amount)


OFFER_STRATEGIES = {
    SpecialOfferType.THREE_FOR_TWO: ThreeForTwoStrategy(),
    SpecialOfferType.TEN_PERCENT_DISCOUNT: PercentDiscountStrategy(),
    SpecialOfferType.TWO_FOR_AMOUNT: BundleForAmountStrategy(2, floor_bundle_count=False),
    SpecialOfferType.FIVE_FOR_AMOUNT: BundleForAmountStrategy(5, floor_bundle_count=True),
}
