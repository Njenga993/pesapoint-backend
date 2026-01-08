import pytest
from django.core.exceptions import ValidationError

from apps.sales.services.sales_service import SalesService
from apps.products.models import Inventory
from apps.sales.models import Order


@pytest.mark.django_db
def test_finalize_order_fails_if_inventory_insufficient(
    business,
    product,
    order_with_items
):
    Inventory.objects.create(
        business=business,
        product=product,
        quantity=1  # less than required
    )

    with pytest.raises(ValidationError):
        SalesService.finalize_order(order_with_items)

    order_with_items.refresh_from_db()
    assert order_with_items.status == Order.STATUS_DRAFT
