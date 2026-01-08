from django.db import models
from apps.businesses.models import Business


class Category(models.Model):
    """
    Product grouping per business.
    Example: Beverages, Groceries, Electronics
    """

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('business', 'name')
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name} ({self.business})"
    
class Product(models.Model):
    """
    Sellable item within a business.
    """

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('business', 'name')
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name
    
class Inventory(models.Model):
    """
    Current stock level for a product within a business.
    """

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='inventory_items'
    )
    product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE,
    related_name='inventory_items'
    )
    quantity = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['business', 'product'],
                name='unique_inventory_per_business_product'
            )
        ]
        indexes = [
            models.Index(fields=['business', 'product']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class InventoryTransaction(models.Model):
    """
    Records every stock movement for auditing.
    """

    TRANSACTION_IN = 'in'
    TRANSACTION_OUT = 'out'
    TRANSACTION_ADJUST = 'adjust'

    TRANSACTION_CHOICES = [
        (TRANSACTION_IN, 'Stock In'),
        (TRANSACTION_OUT, 'Stock Out'),
        (TRANSACTION_ADJUST, 'Adjustment'),
    ]

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='inventory_transactions'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory_transactions'
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES
    )
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['business', '-created_at']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} - {self.product.name}"


