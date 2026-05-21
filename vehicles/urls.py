from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, AdminVehicleViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'admin/vehicles', AdminVehicleViewSet,
                basename='admin-vehicle')

urlpatterns = [
    path('', include(router.urls)),
]
