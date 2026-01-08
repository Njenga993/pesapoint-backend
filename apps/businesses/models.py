from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Business(models.Model):
    """
    Represents a tenant in the PesaPoint system.
    Example: a shop, restaurant, pharmacy, etc.
    """

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='owned_businesses'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"

    def __str__(self):
        return self.name



class BusinessUser(models.Model):
    """
    Associates a user with a business and a role.
    Example: cashier, manager, owner
    """

    ROLE_OWNER = 'owner'
    ROLE_MANAGER = 'manager'
    ROLE_CASHIER = 'cashier'

    ROLE_CHOICES = [
        (ROLE_OWNER, 'Owner'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_CASHIER, 'Cashier'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='business_memberships'
    )
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='members'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['business', 'user'],
                name='unique_user_per_business'
            )
        ]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['business']),
        ]

    def __str__(self):
        return f"{self.user} - {self.business} ({self.role})"
