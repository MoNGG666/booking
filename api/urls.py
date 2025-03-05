from rest_framework.routers import DefaultRouter
from api.views import UserModelViewSet, WarehouseModelViewSet, ProductModelViewSet, TransactionModelViewSet

router = DefaultRouter()
router.register('users', UserModelViewSet)
router.register('warehouses', WarehouseModelViewSet)
router.register('products', ProductModelViewSet)
router.register('transactions', TransactionModelViewSet)

urlpatterns = []
urlpatterns += router.urls