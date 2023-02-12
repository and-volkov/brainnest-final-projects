import re
import logging
from dataclasses import dataclass

log_level = logging.INFO
logger = logging.getLogger("main")
logging.basicConfig(
    filename="orders_parser.log",
    encoding="utf-8",
    level=log_level,
    format="%(asctime)s %(levelname)s: %(name)s: %(message)s",
)


@dataclass
class Order:
    """Order class."""

    order_id: int
    customer: str
    items: dict

    def __str__(self):
        """String representation of object."""
        return (
            f"Order #{self.order_id} Customer:"
            f" {self.customer} Items: {self.items}"
        )

    def to_json(self):
        """Return JSON representation of object."""
        return {
            "Order No": self.order_id,
            "Customer": self.customer,
            "Items": self.items,
        }


class OrdersParser:
    """Parser class."""

    def __init__(self, orders_file):
        self.orders_file = orders_file
        self.orders = []

    def _parse_line(self, line):
        """Parse line and add order to orders list."""
        order_id = re.search(r"Order #(\d+)", line)  # digits
        customer = re.search(r"Customer: (.+?) Items:", line)  # any char
        items = re.search(r"Items: (.+)", line)  # any char
        if order_id and customer and items:
            order_id = int(order_id.group(1))
            customer = customer.group(1)
            items = items.group(1)
            items = items.split(",")  # list of items
            items = {item.strip(): items.count(item) for item in items}  # dict
            order = Order(order_id, customer, items)  # create order
            self.orders.append(order)

    def parse(self):
        """Parse orders file."""
        with open(self.orders_file, "r") as f:
            for line in f:
                self._parse_line(line)


if __name__ == "__main__":
    try:
        parser = OrdersParser("example.txt")
        parser.parse()
        print("\n".join([str(order.to_json()) for order in parser.orders]))
    except Exception as e:
        logger.exception(e)
        print("Something went wrong. Check logs for details.")
        pass
