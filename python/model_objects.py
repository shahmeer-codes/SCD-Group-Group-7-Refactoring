from enum import Enum


class Product:
    """Represents a catalog product with a name and measurement unit."""

    def __init__(self, name, unit):
        self.name = name
        self.unit = unit

    def __repr__(self):
        return f"Product(name={self.name!r}, unit={self.unit!r})"


class ProductQuantity:
    """Associates a Product with a purchased quantity."""

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def __repr__(self):
        return f"ProductQuantity(product={self.product!r}, quantity={self.quantity!r})"


class ProductUnit(Enum):
    EACH = 1
    KILO = 2


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4


class Offer:
    """Represents a promotional offer configured for a product."""

    def __init__(self, offer_type, product, argument):
        self.offer_type = offer_type
        self.product = product
        self.argument = argument

    def __repr__(self):
        return (
            f"Offer(offer_type={self.offer_type!r}, "
            f"product={self.product!r}, argument={self.argument!r})"
        )


class Discount:
    """Represents a calculated discount applied to a Receipt."""

    def __init__(self, product, description, discount_amount):
        self.product = product
        self.description = description
        self.discount_amount = discount_amount

    def __repr__(self):
        return (
            f"Discount(product={self.product!r}, "
            f"description={self.description!r}, "
            f"discount_amount={self.discount_amount!r})"
        )
