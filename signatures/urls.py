from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ElectronicSignatureViewSet

router = DefaultRouter()
router.register(r'electronic-signatures', ElectronicSignatureViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
