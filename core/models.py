# core/models.py

from django.db import models
from core.permissions import PERMISSIONS


class PermissionAnchor(models.Model):
    """
    Dummy model to anchor system-wide permissions.
    """

    class Meta:
        managed = False
        default_permissions = ()
        permissions = [
            (code.replace(".", "_"), label)
            for code, label in PERMISSIONS.items()
        ]
