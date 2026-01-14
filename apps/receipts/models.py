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
    
class ReceiptPrintLog(models.Model):
    METHOD_PDF = "pdf"
    METHOD_THERMAL = "thermal"

    METHOD_CHOICES = [
        (METHOD_PDF, "PDF"),
        (METHOD_THERMAL, "Thermal"),
    ]

    receipt = models.ForeignKey(
        "receipts.Receipt",
        on_delete=models.PROTECT,
        related_name="print_logs",
    )

    printed_by = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="User who initiated the print",
    )

    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
    )

    printer_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional printer identifier",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Receipt Print Log"
        verbose_name_plural = "Receipt Print Logs"

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Print logs are immutable.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Print logs cannot be deleted.")

    def __str__(self):
        return f"{self.receipt.receipt_number} printed via {self.method}"

