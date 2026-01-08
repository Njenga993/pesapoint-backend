from django.contrib import admin
from .models import Category, Product, Inventory, InventoryTransaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'is_active')
    list_filter = ('business', 'is_active')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'price', 'is_active')
    list_filter = ('business', 'is_active')
    search_fields = ('name', 'sku')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'business', 'quantity', 'updated_at')
    list_filter = ('business',)


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'business',
        'transaction_type',
        'quantity',
        'created_at'
    )
    list_filter = ('transaction_type', 'business')
