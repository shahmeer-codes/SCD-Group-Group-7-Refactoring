from model_objects import ProductUnit


class ReceiptFormatter:
    """Formats receipt values (prices, quantities, discount labels) independent of layout."""

    def format_price(self, price):
        return f"{price:.2f}"

    def format_quantity(self, item):
        if ProductUnit.EACH == item.product.unit:
            return str(item.quantity)
        return f"{item.quantity:.3f}"

    def format_discount_label(self, discount):
        return f"{discount.description} ({discount.product.name})"


class ReceiptPrinter:
    """Renders a Receipt into a fixed-width plain-text ticket."""

    DEFAULT_COLUMNS = 40
    SINGLE_ITEM_QUANTITY = 1

    def __init__(self, columns=DEFAULT_COLUMNS, formatter=None):
        self.columns = columns
        self.formatter = formatter or ReceiptFormatter()

    def print_receipt(self, receipt):
        lines = [self.print_receipt_item(item) for item in receipt.items]
        lines.extend(self.print_discount(discount) for discount in receipt.discounts)
        lines.append("\n")
        lines.append(self.present_total(receipt))
        return "".join(lines)

    def print_receipt_item(self, item):
        total_price_printed = self.print_price(item.total_price)
        line = self.format_line_with_whitespace(item.product.name, total_price_printed)
        if item.quantity != self.SINGLE_ITEM_QUANTITY:
            line += f"  {self.print_price(item.price)} * {self.print_quantity(item)}\n"
        return line

    def format_line_with_whitespace(self, name, value):
        whitespace_size = max(0, self.columns - len(name) - len(value))
        return f"{name}{' ' * whitespace_size}{value}\n"

    def print_price(self, price):
        return self.formatter.format_price(price)

    def print_quantity(self, item):
        return self.formatter.format_quantity(item)

    def print_discount(self, discount):
        name = self.formatter.format_discount_label(discount)
        value = self.print_price(discount.discount_amount)
        return self.format_line_with_whitespace(name, value)

    def present_total(self, receipt):
        name = "Total: "
        value = self.print_price(receipt.total_price())
        return self.format_line_with_whitespace(name, value)
