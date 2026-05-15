"""OrderItem entity"""

from src.order_module.product import Product


class OrderItem:
    """Order item with quantity and associated product"""

    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        self.product = product
        self.quantity = quantity
