from model_objects import ProductQuantity
from offer_strategies import OFFER_STRATEGIES


class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_quantities = {}

    @property
    def items(self):
        return self._items

    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities:
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt, offers, catalog):
        for product, quantity in self._product_quantities.items():
            offer = offers.get(product)
            if offer is None:
                continue
            strategy = OFFER_STRATEGIES.get(offer.offer_type)
            if strategy is None:
                continue
            unit_price = catalog.unit_price(product)
            discount = strategy.calculate_discount(
                product, quantity, unit_price, offer.argument
            )
            if discount:
                receipt.add_discount(discount)
