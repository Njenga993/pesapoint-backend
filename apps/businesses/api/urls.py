from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .business_viewset import BusinessViewSet
from .business_user_viewset import BusinessUserViewSet
from .business_settings_viewset import BusinessSettingsViewSet


router = DefaultRouter()
router.register("businesses", BusinessViewSet, basename="business")
router.register("business-users", BusinessUserViewSet, basename="business-user")



urlpatterns = [
    path("", include(router.urls)),
    path(
        "settings/",
        BusinessSettingsViewSet.as_view({
            "get": "retrieve",
            "patch": "partial_update",
        }),
        name="business-settings",
    ),
]
