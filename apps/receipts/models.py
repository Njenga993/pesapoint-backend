from django.db import models
from django.core.exceptions import ValidationError


class Receipt(models.Model):
    """
    Immutable receipt generated after payment finalization.
    A PDF version is generated once and stored permanently.
    """

    payment = models.OneToOneField(
        "sales.Payment",
        on_delete=models.PROTECT,
        related_name="receipt",
    )

    receipt_number = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
    )

    pdf = models.FileField(
        upload_to="receipts/pdfs/",
        null=True,
        blank=True,
        editable=False,
        help_text="Generated PDF receipt (immutable)",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Receipt"
        verbose_name_plural = "Receipts"

    # -------------------------
    # Immutability Enforcement
    # -------------------------
    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Receipts are immutable and cannot be modified.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Receipts cannot be deleted.")

    # -------------------------
    # Utilities
    # -------------------------
    @property
    def has_pdf(self):
        return bool(self.pdf)

    def __str__(self):
        return f"Receipt {self.receipt_number}"
