from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .user_viewset import UserViewSet
from .ledger_viewset import LedgerViewSet
from .account_viewset import AccountViewSet
from .reports_viewset import ReportsViewSet
from .roles_viewset import RoleViewSet
from .permissions_viewset import PermissionViewSet


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"roles", RoleViewSet, basename="role")
router.register("ledger", LedgerViewSet, basename="ledger")
router.register("accounts", AccountViewSet, basename="account")
router.register("reports", ReportsViewSet, basename="report")
router.register("permissions", PermissionViewSet, basename="permissions")


urlpatterns = [
    path("", include(router.urls)),
]
