"""Order entity"""


class Order:
    """Order with pricing information and received items"""

    def __init__(
        self, total_amount: float = 0, original_amount: float = 0, discount: float = 0
    ):
        self.total_amount = total_amount
        self.original_amount = original_amount
        self.discount = discount
        # Items received by customer (including complimentary items from promotions)
        self.received_items = []  # List of (product_name, quantity)
