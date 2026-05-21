from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductPhotoViewSet

router = DefaultRouter()
router.register(r'product-photos', ProductPhotoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
