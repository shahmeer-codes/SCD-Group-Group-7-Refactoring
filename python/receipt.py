class ReceiptItem:
    """Line item recorded on a Receipt."""

    def __init__(self, product, quantity, price, total_price):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price

    def __repr__(self):
        return (
            f"ReceiptItem(product={self.product!r}, quantity={self.quantity!r}, "
            f"price={self.price!r}, total_price={self.total_price!r})"
        )


class Receipt:
    """Aggregates purchased items and applied discounts for a checkout."""

    def __init__(self):
        self._items = []
        self._discounts = []

    def items_total(self):
        """Return the sum of all item line totals before discounts."""
        return sum(item.total_price for item in self._items)

    def discounts_total(self):
        """Return the sum of all applied discount amounts."""
        return sum(discount.discount_amount for discount in self._discounts)

    def total_price(self):
        """Return the net total price (items plus negative discounts)."""
        return self.items_total() + self.discounts_total()

    def add_product(self, product, quantity, price, total_price):
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount):
        self._discounts.append(discount)

    @property
    def items(self):
        return self._items[:]

    @property
    def discounts(self):
        return self._discounts[:]
