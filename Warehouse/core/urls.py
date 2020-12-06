from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import WarehousesListAPIView, WarehouseOrderViewSet

app_name = 'core'

router = DefaultRouter()
router.register('syncWH', WarehouseOrderViewSet, basename='core')

urlpatterns = [
    path('warehouses/', WarehousesListAPIView.as_view()),
] + router.urls
