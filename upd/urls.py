from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UPDViewSet

router = DefaultRouter()
router.register(r'upd', UPDViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
