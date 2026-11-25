
class SupermarketCatalog:
    """Base catalog interface representing the supermarket product database."""

    def add_product(self, product, price):
        raise Exception("cannot be called from a unit test - it accesses the database")

    def unit_price(self, product):
        raise Exception("cannot be called from a unit test - it accesses the database")

    def product_with_name(self, name):
        raise Exception("cannot be called from a unit test - it accesses the database")


