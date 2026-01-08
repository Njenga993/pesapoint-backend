import pytest
from django.contrib.auth import get_user_model
from apps.businesses.models import Business, BusinessUser
from apps.products.models import Product, Category
from apps.sales.models import Order, OrderItem
from apps.accounts.models import Account

User = get_user_model()


@pytest.fixture
def user():
    """
    Create a test user.

    NOTE:
    - Username is required because the current User model still expects it.
    - Email is included because the rest of the system relies on email identity.
    """
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="password123"
    )


@pytest.fixture
def business(user):
    business = Business.objects.create(
        name="Test Business",
        owner=user
    )
    BusinessUser.objects.create(
        business=business,
        user=user,
        role=BusinessUser.ROLE_OWNER
    )
    return business


@pytest.fixture
def category(business):
    return Category.objects.create(
        name="Category",
        business=business
    )


@pytest.fixture
def product(business, category):
    return Product.objects.create(
        business=business,
        category=category,
        name="Test Product",
        price=100
    )


@pytest.fixture
def order_with_items(business, product):
    order = Order.objects.create(
        business=business
    )
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=2,
        price=100
    )
    return order

@pytest.fixture
def chart_of_accounts(db):
    accounts = {
        "AR": Account.objects.create(code="AR", name="Accounts Receivable"),
        "CASH": Account.objects.create(code="CASH", name="Cash"),
        "REV": Account.objects.create(code="REV", name="Revenue"),
        "REFUND": Account.objects.create(code="REFUND", name="Refunds"),
    }
    return accounts