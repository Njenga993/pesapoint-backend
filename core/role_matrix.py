# core/role_matrix.py

ROLE_MATRIX = {
    "Super Admin": [
        "users.create_user",
        "users.update_user",
        "users.disable_user",
        "users.assign_roles",
        "users.view_users",
        "audit.view_logs",
        "audit.view_print_logs",
        "config.update_settings",
        "config.view_settings",
        "printers.register_printer",
        "printers.assign_printer",
        "printers.view_printers",
    ],

    "Finance Admin": [
        "payments.refund_payment",
        "reports.view_financials",
        "audit.view_logs",
        "audit.view_print_logs",
    ],

    "Manager": [
        "sales.cancel_order",
        "reports.view_sales",
        "reports.view_financials",
        "audit.view_print_logs",
    ],

    "Cashier": [
        "sales.create_order",
        "sales.update_order",
        "payments.record_payment",
        "receipts.generate_pdf",
        "receipts.print_pdf",
        "receipts.print_thermal",
        "receipts.view_receipt",
    ],

    "Auditor": [
        "users.view_users",
        "sales.view_orders",
        "payments.view_payments",
        "receipts.view_receipt",
        "reports.view_sales",
        "reports.view_financials",
        "audit.view_logs",
        "audit.view_print_logs",
    ],

    "System": [
        "system.run_jobs",
    ],
}
