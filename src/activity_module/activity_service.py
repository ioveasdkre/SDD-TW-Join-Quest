"""ActivityService for checkout and promotion calculation"""

from typing import List

from src.activity_module.entities import Activity, ActivityOrder, CartItem


class ActivityService:
    """Service to handle checkout with double 11 promotion"""

    def __init__(self):
        """Initialize service"""
        self.activity: Activity = None

    def set_activity(self, threshold_quantity: int, discount_amount: float):
        """Set up the double 11 promotion activity"""
        self.activity = Activity(threshold_quantity, discount_amount)

    def checkout(self, items: List[CartItem]) -> ActivityOrder:
        """
        Process checkout and apply double 11 promotion

        Promotion rule: For each product type, if quantity >= threshold_quantity,
        apply discount_amount to that product's subtotal.

        Args:
            items: List of CartItem in the cart

        Returns:
            ActivityOrder with calculated total and items
        """
        # Calculate original total
        original_total = sum(item.get_subtotal() for item in items)

        # Apply promotion discounts
        total_discount = 0
        if self.activity is not None:
            for item in items:
                # Check if this item qualifies for discount
                if item.quantity >= self.activity.threshold_quantity:
                    # Apply discount to this item
                    total_discount += self.activity.discount_amount

        # Calculate final total
        final_total = original_total - total_discount

        # Create order
        order = ActivityOrder(
            total_amount=final_total,
            original_amount=original_total,
            discount=total_discount,
        )

        # Add items to order
        for item in items:
            order.items.append((item.name, item.quantity))

        return order
