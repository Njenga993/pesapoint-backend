from rest_framework.routers import DefaultRouter

from apps.sales.api.order_viewset import OrderViewSet
from apps.sales.api.payment_viewset import PaymentViewSet

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = router.urls
