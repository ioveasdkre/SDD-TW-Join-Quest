"""OrderService for order checkout and promotion logic"""

from typing import List, Optional

from src.order_module.order import Order
from src.order_module.order_item import OrderItem
from src.order_module.promotions import BuyOneGetOnePromotion, ThresholdDiscount


class OrderService:
    """Service to handle order checkout and calculate totals with promotions"""

    def __init__(self):
        """Initialize order service"""
        self.threshold_discount: Optional[ThresholdDiscount] = None
        self.bogo_promotions: List[BuyOneGetOnePromotion] = []

    def set_threshold_discount(self, threshold: float, discount: float):
        """Configure threshold discount promotion"""
        self.threshold_discount = ThresholdDiscount(threshold, discount)

    def add_bogo_promotion(self, category: str):
        """Add buy one get one promotion for a category"""
        self.bogo_promotions.append(BuyOneGetOnePromotion(category))

    def _calculate_received_quantity(
        self, product_category: str, purchased_quantity: int
    ) -> int:
        """Calculate actual quantity received after applying BOGO promotions"""
        # Check if this category has an active BOGO promotion
        has_bogo = any(
            promo.category == product_category for promo in self.bogo_promotions
        )

        if has_bogo and product_category == "cosmetics":
            # Buy-one-get-one: purchased N + receive ceil(N/2) = N + (N+1)//2
            return purchased_quantity + (purchased_quantity + 1) // 2

        return purchased_quantity

    def _apply_threshold_discount(self, total_amount: float) -> int:
        """Calculate discount based on threshold promotion if applicable"""
        if not self.threshold_discount:
            return 0

        if total_amount >= self.threshold_discount.threshold:
            return self.threshold_discount.discount

        return 0

    def checkout(self, items: List[OrderItem]) -> Order:
        """
        Process checkout for items and apply promotions

        Args:
            items: List of OrderItem to checkout

        Returns:
            Order with calculated total amount and discounts
        """
        # Calculate total and build received items list
        total_amount = 0
        received_items_map = {}

        for item in items:
            item_total = item.quantity * item.product.unit_price
            total_amount += item_total

            # Apply BOGO to calculate what customer receives
            quantity_received = self._calculate_received_quantity(
                item.product.category, item.quantity
            )
            received_items_map[item.product.name] = quantity_received

        # Store original amount before discounts
        original_amount = total_amount

        # Apply threshold discount if applicable
        discount = self._apply_threshold_discount(total_amount)
        total_amount -= discount

        # Create order with received items
        order = Order(
            total_amount=total_amount,
            original_amount=original_amount,
            discount=discount,
        )
        order.received_items = list(received_items_map.items())

        return order
