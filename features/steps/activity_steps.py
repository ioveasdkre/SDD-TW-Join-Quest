"""Step definitions for activity management scenarios"""

from behave import given, then, when

from src.activity_module.activity_service import ActivityService
from src.activity_module.entities import CartItem


@given("購物車內包含以下商品")
def step_cart_contains_items(context):
    """Initialize shopping cart with items"""
    context.activity_service = ActivityService()
    context.items = []

    for row in context.table:
        name = row["商品名稱"]
        quantity = int(row["數量"])
        unit_price = int(row["單價"])

        cart_item = CartItem(name, quantity, unit_price)
        context.items.append(cart_item)


@given("雙十一優惠已啟用")
def step_activity_enabled(context):
    """Enable double 11 promotion activity"""
    # Get or create activity service
    if not hasattr(context, "activity_service") or context.activity_service is None:
        context.activity_service = ActivityService()

    # Parse promotion config
    for row in context.table:
        threshold = int(row["門檻數量"])
        discount = int(row["折扣金額"])
        context.activity_service.set_activity(threshold, discount)


@when("結帳")
def step_checkout(context):
    """Process checkout"""
    if not hasattr(context, "activity_service") or context.activity_service is None:
        context.activity_service = ActivityService()

    context.order = context.activity_service.checkout(context.items)


@then("訂單總金額應為 {amount:d}")
def step_verify_total_amount(context, amount):
    """Verify order total amount"""
    assert context.order.total_amount == amount, (
        f"Expected total {amount}, got {context.order.total_amount}"
    )


@then("訂單應包含以下商品")
def step_verify_order_items(context):
    """Verify order contains expected items"""
    expected_items = {}

    for row in context.table:
        name = row["商品名稱"]
        quantity = int(row["數量"])
        expected_items[name] = quantity

    # Build actual items map
    actual_items = {}
    if hasattr(context.order, "items") and context.order.items:
        for name, quantity in context.order.items:
            actual_items[name] = quantity

    # Verify
    for name, expected_qty in expected_items.items():
        actual_qty = actual_items.get(name, 0)
        assert actual_qty == expected_qty, (
            f"Expected {expected_qty} of {name}, got {actual_qty}"
        )
