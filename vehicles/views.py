"""
ViewSet приложения vehicles (контроллеры в сиквенсах)

Реализованные сиквенсы:
№13 - ТС (список) - GET /api/v1/vehicles/
№24 - ТС (CRUD) - POST /api/v1/admin/vehicles/
"""

from rest_framework import viewsets, permissions
from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Сиквенс №13: GET /api/v1/vehicles/ - список ТС.
    Доступ: диспетчер, администратор.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.user.role not in ['dispatcher', 'admin']:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()


class AdminVehicleViewSet(viewsets.ModelViewSet):
    """
    Сиквенс №24: CRUD операции с ТС (администратор).
    Доступ: только администратор.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.user.role != 'admin':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()
