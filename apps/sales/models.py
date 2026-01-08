from django.db import models
from apps.businesses.models import Business
from apps.products.models import Product
from django.conf import settings


class Order(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    PAYMENT_UNPAID = "unpaid"
    PAYMENT_PARTIAL = "partial"
    PAYMENT_PAID = "paid"

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_UNPAID, "Unpaid"),
        (PAYMENT_PARTIAL, "Partially Paid"),
        (PAYMENT_PAID, "Paid"),
    ]

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_UNPAID,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['business', '-created_at']),
            models.Index(fields=['business', 'status']),
            models.Index(fields=['business', 'payment_status']),
        ]

    def __str__(self):
        return f"Order #{self.id} ({self.status}, {self.payment_status})"



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['order']),
        ]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    

class Payment(models.Model):
    """
    Records payments and refunds for an order.
    Immutable once completed.
    """

    # Direction
    DIRECTION_IN = 'in'
    DIRECTION_OUT = 'out'  # refunds

    DIRECTION_CHOICES = [
        (DIRECTION_IN, 'Payment'),
        (DIRECTION_OUT, 'Refund'),
    ]

    # Method
    METHOD_CASH = 'cash'
    METHOD_MPESA = 'mpesa'
    METHOD_CARD = 'card'

    METHOD_CHOICES = [
        (METHOD_CASH, 'Cash'),
        (METHOD_MPESA, 'MPesa'),
        (METHOD_CARD, 'Card'),
    ]

    # Status
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_REVERSED = 'reversed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_REVERSED, 'Reversed'),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    direction = models.CharField(
        max_length=5,
        choices=DIRECTION_CHOICES,
        default=DIRECTION_IN
    )

    method = models.CharField(
        max_length=10,
        choices=METHOD_CHOICES
    )

    amount = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    reference = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    finalized_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.direction} {self.amount} ({self.status})"

