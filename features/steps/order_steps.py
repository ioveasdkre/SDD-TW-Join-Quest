"""Step definitions for order pricing scenarios"""

from behave import given, then, when

from src.order_module.order_item import OrderItem
from src.order_module.order_service import OrderService
from src.order_module.product import Product


@given("no promotions are applied")
def step_no_promotions(context):
    """Set up context with no promotions"""
    context.order_service = OrderService()
    context.items = []
    context.order = None


@given("the threshold discount promotion is configured:")
def step_threshold_discount_configured(context):
    """Configure threshold discount promotion"""
    # Create order service if not already created
    if not hasattr(context, "order_service") or context.order_service is None:
        context.order_service = OrderService()

    # Parse the data table and configure the service
    for row in context.table:
        threshold = int(row["threshold"])
        discount = int(row["discount"])
        context.order_service.set_threshold_discount(threshold, discount)


@given("the buy one get one promotion for cosmetics is active")
def step_buy_one_get_one_active(context):
    """Activate buy one get one promotion for cosmetics"""
    # Create order service if not already created
    if not hasattr(context, "order_service") or context.order_service is None:
        context.order_service = OrderService()

    # Add the BOGO promotion
    context.order_service.add_bogo_promotion("cosmetics")


@when("a customer places an order with:")
def step_customer_places_order(context):
    """Process order with items from data table"""
    context.items = []

    for row in context.table:
        product_name = row["productName"]
        quantity = int(row["quantity"])
        unit_price = int(row["unitPrice"])

        # Handle optional category column
        category = row.get("category", "")

        product = Product(product_name, unit_price, category)
        order_item = OrderItem(product, quantity)
        context.items.append(order_item)

    # Use existing order service if configured, otherwise create a new one
    if not hasattr(context, "order_service") or context.order_service is None:
        context.order_service = OrderService()

    # Checkout the order
    context.order = context.order_service.checkout(context.items)


@then("the order summary should be:")
def step_order_summary(context):
    """Verify order summary details"""
    for row in context.table:
        # Get column names from the table header
        columns = context.table.headings

        if "totalAmount" in columns:
            expected_total = int(row["totalAmount"])
            assert context.order.total_amount == expected_total, (
                f"Expected total {expected_total}, got {context.order.total_amount}"
            )

        if "originalAmount" in columns:
            expected_original = int(row["originalAmount"])
            assert context.order.original_amount == expected_original, (
                f"Expected original {expected_original}, got {context.order.original_amount}"
            )

        if "discount" in columns:
            expected_discount = int(row["discount"])
            assert context.order.discount == expected_discount, (
                f"Expected discount {expected_discount}, got {context.order.discount}"
            )


@then("the customer should receive:")
def step_customer_receives(context):
    """Verify the items the customer receives (including promotional items)"""
    expected_items = {}

    for row in context.table:
        product_name = row["productName"]
        expected_quantity = int(row["quantity"])
        expected_items[product_name] = expected_quantity

    # Get actual received items from the order
    actual_items = {}
    if hasattr(context.order, "received_items") and context.order.received_items:
        for product_name, quantity in context.order.received_items:
            actual_items[product_name] = quantity
    else:
        # Fallback to ordered items if received_items not populated
        for item in context.items:
            if item.product.name in actual_items:
                actual_items[item.product.name] += item.quantity
            else:
                actual_items[item.product.name] = item.quantity

    for product_name, expected_qty in expected_items.items():
        actual_qty = actual_items.get(product_name, 0)
        assert actual_qty == expected_qty, (
            f"Expected {expected_qty} of {product_name}, got {actual_qty}"
        )
