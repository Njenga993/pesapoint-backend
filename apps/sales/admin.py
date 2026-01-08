from django.contrib import admin
from .models import Order, OrderItem, Payment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'business',
        'status',
        'created_at',
    )
    list_filter = ('status', 'business')
    readonly_fields = ('created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
        'price',
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'direction',
        'method',
        'amount',
        'status',
        'created_at',
        'finalized_at',
    )

    list_filter = (
        'status',
        'method',
        'direction',
    )

    readonly_fields = (
        'created_at',
        'finalized_at',
    )

