# apps/accounts/serializers/ledger.py
from rest_framework import serializers
from apps.accounts.models import LedgerEntry
from apps.accounts.models import Account


class LedgerEntrySerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(
        source="account.name",
        read_only=True,
    )

    class Meta:
        model = LedgerEntry
        fields = [
            "id",
            "account_name",
            "debit",
            "credit",
            "created_at",
        ]
        read_only_fields = fields

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'code', 'name']
        read_only_fields = fields        
