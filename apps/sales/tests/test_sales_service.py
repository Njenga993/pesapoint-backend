import pytest
from apps.sales.services.sales_service import SalesService 
from apps.products.models import Inventory
from apps.sales.models import Order
from apps.products.models import InventoryTransaction


@pytest.mark.django_db
def test_finalize_order_deducts_inventory(
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
    inventory.refresh_from_db()

    assert inventory.quantity == 8
    assert order_with_items.status == Order.STATUS_COMPLETED

