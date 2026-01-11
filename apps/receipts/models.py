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
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    # -------------------------
    # Controlled immutability
    # -------------------------
    def save(self, *args, **kwargs):
        if self.pk:
            original = Receipt.objects.get(pk=self.pk)

            # ❌ Block changes EXCEPT first-time PDF attachment
            if original.pdf and original.pdf != self.pdf:
                raise ValidationError("Receipts are immutable once PDF is generated.")

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Receipts cannot be deleted.")

    @property
    def has_pdf(self):
        return bool(self.pdf)

    def __str__(self):
        return f"Receipt {self.receipt_number}"
