"""
Маршруты приложения users
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DriverViewSet, AdminUserViewSet, CurrentUserViewSet

router = DefaultRouter()
router.register(r'drivers', DriverViewSet, basename='driver')
router.register(r'admin/users', AdminUserViewSet, basename='admin-user')

urlpatterns = [
    path('', include(router.urls)),
    path('users/me/',
         CurrentUserViewSet.as_view({'get': 'list'}), name='current-user'),
]
