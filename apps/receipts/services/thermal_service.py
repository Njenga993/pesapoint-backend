from dataclasses import dataclass

from django.core.exceptions import ValidationError

from apps.receipts.models import Receipt


# -------------------------
# ESC/POS CONSTANTS
# -------------------------
ESC = b"\x1b"
GS = b"\x1d"
LF = b"\n"


def escpos_init():
    return ESC + b"@"


def escpos_align(mode: str):
    modes = {
        "left": b"\x00",
        "center": b"\x01",
        "right": b"\x02",
    }
    return ESC + b"a" + modes[mode]


def escpos_bold(on: bool):
    return ESC + b"E" + (b"\x01" if on else b"\x00")


def escpos_cut():
    return GS + b"V\x01"


# -------------------------
# OUTPUT PAYLOAD
# -------------------------
@dataclass(frozen=True)
class ThermalPrintPayload:
    escpos: bytes
    text: str
    paper_width: int  # mm (usually 80 or 58)


# -------------------------
# SERVICE
# -------------------------
class ThermalReceiptService:
    """
    Generates printer-ready thermal receipt payloads (ESC/POS).
    READ-ONLY service: must not mutate receipt state.
    """

    PAPER_WIDTH_MM = 80
    LINE_WIDTH = 42

    @staticmethod
    def generate_payload(receipt: Receipt) -> ThermalPrintPayload:
        if receipt is None:
            raise ValidationError("Receipt is required")

        if receipt.pk is None:
            raise ValidationError("Receipt must be saved")

        # 🔑 CRITICAL LINE — normalize FileField representation
        _ = receipt.pdf

        if receipt.payment_id is None:
            raise ValidationError("Receipt has no payment")

        payment = receipt.payment
        order = getattr(payment, "order", None)

        def center(text: str) -> str:
            return text.center(ThermalReceiptService.LINE_WIDTH)

        def divider() -> str:
            return "-" * ThermalReceiptService.LINE_WIDTH

        lines = [
            center("PESAPOINT"),
            divider(),
            f"Receipt: {receipt.receipt_number}",
            f"Date: {receipt.created_at.strftime('%Y-%m-%d %H:%M')}",
            divider(),
        ]

        if order:
            lines.append(f"Order ID: {order.id}")

        lines.extend(
            [
                f"Payment Method: {payment.method}",
                f"Amount Paid: {payment.amount}",
                divider(),
                center("Thank you for your business!"),
            ]
        )

        text_output = "\n".join(lines)

        escpos = b""
        escpos += escpos_init()
        escpos += escpos_align("center")
        escpos += escpos_bold(True)
        escpos += b"PESAPOINT\n"
        escpos += escpos_bold(False)
        escpos += escpos_align("left")

        escpos += divider().encode() + LF
        escpos += f"Receipt: {receipt.receipt_number}".encode() + LF
        escpos += f"Date: {receipt.created_at.strftime('%Y-%m-%d %H:%M')}".encode() + LF
        escpos += divider().encode() + LF

        if order:
            escpos += f"Order ID: {order.id}".encode() + LF

        escpos += f"Payment Method: {payment.method}".encode() + LF
        escpos += f"Amount Paid: {payment.amount}".encode() + LF
        escpos += divider().encode() + LF

        escpos += escpos_align("center")
        escpos += b"Thank you!\n\n"
        escpos += escpos_cut()

        return ThermalPrintPayload(
            escpos=escpos,
            text=text_output,
            paper_width=ThermalReceiptService.PAPER_WIDTH_MM,
        )

