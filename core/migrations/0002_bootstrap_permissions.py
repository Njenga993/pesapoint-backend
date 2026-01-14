from django.db import migrations


def bootstrap_permissions(apps, schema_editor):
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    from core.permissions import PERMISSIONS

    content_type, _ = ContentType.objects.get_or_create(
        app_label="core",
        model="permission"
    )

    for full_code, description in PERMISSIONS.items():
        codename = full_code.split(".")[1]

        Permission.objects.get_or_create(
            codename=codename,
            name=description,
            content_type=content_type,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(bootstrap_permissions),
    ]
