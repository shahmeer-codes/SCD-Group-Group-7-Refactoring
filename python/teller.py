from model_objects import Offer
from receipt import Receipt


class Teller:

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}

    def add_special_offer(self, offer_type, product, argument):
        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart):
        receipt = Receipt()
        self._add_cart_items_to_receipt(the_cart, receipt)
        the_cart.handle_offers(receipt, self.offers, self.catalog)
        return receipt

    def _add_cart_items_to_receipt(self, the_cart, receipt):
        """Record each item in the cart on the receipt with its catalog price."""
        for pq in the_cart.items:
            product = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(product)
            price = quantity * unit_price
            receipt.add_product(product, quantity, unit_price, price)

    def product_with_name(self, name):
        return self.catalog.product_with_name(name)