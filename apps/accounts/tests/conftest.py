import pytest
from apps.accounts.models import Account


@pytest.fixture
def chart_of_accounts(db):
    accounts = {
        "AR": Account.objects.create(code="AR", name="Accounts Receivable"),
        "CASH": Account.objects.create(code="CASH", name="Cash"),
        "REV": Account.objects.create(code="REV", name="Revenue"),
        "REFUND": Account.objects.create(code="REFUND", name="Refunds"),
    }
    return accounts
