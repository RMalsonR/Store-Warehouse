from rest_framework.routers import DefaultRouter

from .views import StoreOrderViewSet

app_name = 'core'

router = DefaultRouter()
router.register('syncStore', StoreOrderViewSet, basename='core')

urlpatterns = router.urls
