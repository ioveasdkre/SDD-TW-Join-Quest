"""Product entity"""


class Product:
    """Product with name, unit price, and category"""

    def __init__(self, name: str, unit_price: float, category: str = ""):
        self.name = name
        self.unit_price = unit_price
        self.category = category
