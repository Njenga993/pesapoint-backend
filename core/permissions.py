# core/permissions.py

PERMISSIONS = {
    # Users & Access
    "users.create_user": "Can create users",
    "users.update_user": "Can update users",
    "users.disable_user": "Can disable users",
    "users.assign_roles": "Can assign roles",
    "users.view_users": "Can view users",

    # Sales
    "sales.create_order": "Can create sales orders",
    "sales.update_order": "Can update sales orders",
    "sales.cancel_order": "Can cancel sales orders",
    "sales.view_orders": "Can view sales orders",

    # Payments
    "payments.record_payment": "Can record payments",
    "payments.refund_payment": "Can refund payments",
    "payments.view_payments": "Can view payments",

    # Receipts
    "receipts.generate_pdf": "Can generate receipt PDF",
    "receipts.print_pdf": "Can print receipt PDF",
    "receipts.print_thermal": "Can print thermal receipt",
    "receipts.view_receipt": "Can view receipts",

    # Printing
    "printers.register_printer": "Can register printers",
    "printers.assign_printer": "Can assign printers",
    "printers.view_printers": "Can view printers",

    # Reports
    "reports.view_sales": "Can view sales reports",
    "reports.view_financials": "Can view financial reports",

    # Audit
    "audit.view_logs": "Can view audit logs",
    "audit.view_print_logs": "Can view receipt print logs",

    # System
    "config.update_settings": "Can update system settings",
    "config.view_settings": "Can view system settings",
    "system.run_jobs": "Can run system jobs",
}
