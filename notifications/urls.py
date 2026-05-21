from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, UrgentNotificationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)
router.register(r'urgent-notifications', UrgentNotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
