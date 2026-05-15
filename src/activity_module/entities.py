"""Activity related entities for double 11 promotion"""

from typing import List


class CartItem:
    """Item in shopping cart"""

    def __init__(self, name: str, quantity: int, unit_price: float):
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price

    def get_subtotal(self) -> float:
        """Calculate subtotal for this item"""
        return self.quantity * self.unit_price


class ActivityCart:
    """Shopping cart for double 11 promotion"""

    def __init__(self):
        self.items: List[CartItem] = []

    def add_item(self, name: str, quantity: int, unit_price: float):
        """Add item to cart"""
        self.items.append(CartItem(name, quantity, unit_price))


class Activity:
    """Double 11 promotion activity"""

    def __init__(self, threshold_quantity: int, discount_amount: float):
        self.threshold_quantity = threshold_quantity
        self.discount_amount = discount_amount


class ActivityOrder:
    """Order with activity promotion applied"""

    def __init__(
        self, total_amount: float = 0, original_amount: float = 0, discount: float = 0
    ):
        self.total_amount = total_amount
        self.original_amount = original_amount
        self.discount = discount
        self.items = []  # List of (name, quantity)
