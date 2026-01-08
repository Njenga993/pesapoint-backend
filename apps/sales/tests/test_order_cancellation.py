import pytest
from apps.sales.services.sales_service import SalesService
from apps.sales.models import Order
from apps.products.models import Inventory, InventoryTransaction


@pytest.mark.django_db
def test_cancel_order_restores_inventory(
    business,
    product,
    order_with_items,
    chart_of_accounts

):
    inventory = Inventory.objects.create(
        business=business,
        product=product,
        quantity=10
    )

    SalesService.finalize_order(order_with_items)
    order_with_items.refresh_from_db()
    SalesService.cancel_order(order_with_items)


    inventory.refresh_from_db()
    order_with_items.refresh_from_db()

    assert inventory.quantity == 10
    assert order_with_items.status == Order.STATUS_CANCELLED
    assert InventoryTransaction.objects.count() == 2
