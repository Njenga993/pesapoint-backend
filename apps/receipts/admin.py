from django.contrib import admin
from .models import Receipt


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "receipt_number",
        "payment",
        "created_at",
    )

    search_fields = ("receipt_number",)
    ordering = ("-created_at",)

    readonly_fields = (
        "payment",
        "receipt_number",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
