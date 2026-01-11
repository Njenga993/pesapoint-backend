import io
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from apps.receipts.models import Receipt


class ReceiptPDFService:
    """
    Generates immutable PDF receipts.
    """

    @staticmethod
    def generate(receipt: Receipt) -> ContentFile:
        """
        Generate PDF for a receipt and return as ContentFile.
        """

        if hasattr(receipt, "pdf") and receipt.pdf:
            raise ValidationError("PDF already generated for this receipt")

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        width, height = A4
        y = height - 30 * mm

        payment = receipt.payment
        order = payment.order

        # -------------------------
        # Header
        # -------------------------
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30 * mm, y, "PESAPOINT RECEIPT")

        y -= 10 * mm
        c.setFont("Helvetica", 10)
        c.drawString(30 * mm, y, f"Receipt No: {receipt.receipt_number}")
        y -= 6 * mm
        c.drawString(
            30 * mm,
            y,
            f"Date: {receipt.created_at.strftime('%Y-%m-%d %H:%M')}",
        )

        # -------------------------
        # Payment Info
        # -------------------------
        y -= 12 * mm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(30 * mm, y, "Payment Details")

        y -= 6 * mm
        c.setFont("Helvetica", 10)

        if order:
            c.drawString(30 * mm, y, f"Order ID: {order.id}")
            y -= 5 * mm

        c.drawString(30 * mm, y, f"Payment Method: {payment.method}")
        y -= 5 * mm
        c.drawString(30 * mm, y, f"Amount Paid: {payment.amount}")

        # -------------------------
        # Footer
        # -------------------------
        y -= 20 * mm
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(
            30 * mm,
            y,
            "This receipt was system-generated and is valid without signature.",
        )

        c.showPage()
        c.save()

        buffer.seek(0)

        return ContentFile(
            buffer.read(),
            name=f"{receipt.receipt_number}.pdf",
        )
