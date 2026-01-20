from rest_framework.routers import DefaultRouter

from apps.products.api.category_viewset import CategoryViewSet
from apps.products.api.product_viewset import ProductViewSet
from apps.products.api.inventory_viewset import InventoryTransactionViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("inventory-transactions", InventoryTransactionViewSet, basename="inventory")

urlpatterns = router.urls
