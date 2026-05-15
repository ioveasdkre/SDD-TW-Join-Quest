"""Promotion configurations for orders"""


class ThresholdDiscount:
    """Threshold-based discount promotion"""

    def __init__(self, threshold: float, discount: float):
        self.threshold = threshold
        self.discount = discount


class BuyOneGetOnePromotion:
    """Buy one get one free promotion for a specific category"""

    def __init__(self, category: str):
        self.category = category
