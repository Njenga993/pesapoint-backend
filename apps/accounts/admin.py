from django.contrib import admin

from .models import (
    User,
    Account,
    LedgerEntry,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    """
    Ledger entries are strictly read-only in admin.
    This is an audit surface, not a data entry interface.
    """

    list_display = (
        "created_at",
        "account",
        "debit",
        "credit",
        "entry_type",
        "reference",
    )
    list_filter = ("entry_type", "created_at", "account")
    search_fields = ("reference",)
    ordering = ("-created_at",)

    # 🔒 FULL LOCKDOWN — READ ONLY
    readonly_fields = (
        "order",
        "payment",
        "account",
        "debit",
        "credit",
        "entry_type",
        "reference",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
