from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WaybillViewSet, WaybillGenerateViewSet

router = DefaultRouter()
router.register(r'waybills', WaybillViewSet, basename='waybill')

urlpatterns = [
    path('', include(router.urls)),
    path('waybills/generate/',
         WaybillGenerateViewSet.as_view({'post': 'create'}), name='waybill-generate'),
]
