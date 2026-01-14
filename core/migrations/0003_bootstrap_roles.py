# core/migrations/0003_bootstrap_roles.py

from django.db import migrations
from core.permissions import PERMISSIONS
from core.role_matrix import ROLE_MATRIX


def bootstrap_roles(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    # Map app_label -> model_name for permissions
    APP_MODEL_MAP = {
        "users": "user",
        "sales": "order",
        "payments": "payment",
        "receipts": "receipt",
        "printers": "printer",
        "reports": "report",
        "audit": "log",
        "config": "config",
        "system": "job",
    }

    for role, perm_codes in ROLE_MATRIX.items():
        group, _ = Group.objects.get_or_create(name=role)

        for code in perm_codes:
            try:
                app_label, perm_name = code.split(".")
            except ValueError:
                raise ValueError(f"Invalid permission code format: {code}")

            model_name = APP_MODEL_MAP.get(app_label)
            if not model_name:
                raise ValueError(f"No model mapping found for app_label '{app_label}'")

            # Safely get the ContentType via historical model
            content_type_qs = ContentType.objects.filter(app_label=app_label, model=model_name)
            if not content_type_qs.exists():
                print(f"Skipping permission '{code}': ContentType not found for {app_label}.{model_name}")
                continue  # Skip this permission

            content_type = content_type_qs.first()

            # Get or skip Permission
            perm_qs = Permission.objects.filter(codename=perm_name, content_type=content_type)
            if not perm_qs.exists():
                print(f"Skipping permission '{code}': Permission not found in DB")
                continue

            perm = perm_qs.first()
            group.permissions.add(perm)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_bootstrap_permissions"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(bootstrap_roles),
    ]
