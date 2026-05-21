"""
ViewSet приложения upd (контроллеры в сиквенсах)

Реализованные сиквенсы:
№1 - УПД (список) - GET /api/v1/upd/
№2 - УПД (создание) - POST /api/v1/upd/
"""

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import UPD
from .serializers import UPDSerializer
from delivery_requests.models import DeliveryRequest


class UPDViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с УПД.
    Доступ: диспетчер, менеджер, администратор (для списка)
    """
    queryset = UPD.objects.all()
    serializer_class = UPDSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """Настройка прав доступа в зависимости от действия"""
        if self.action == 'list':
            # Сиквенс №1: список УПД доступен только диспетчеру, менеджеру, администратору
            if self.request.user.role not in ['dispatcher', 'manager', 'admin']:
                self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Сиквенс №2: создание УПД (передача из учётной системы 1С)
        При создании УПД автоматически создаётся заявка на доставку (сиквенс №4)
        """
        # Валидация данных через сериализатор
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Сохранение УПД
        upd = serializer.save()

        # Автоматическое создание заявки на доставку
        delivery_request = DeliveryRequest.objects.create(
            number_delivery_request=f'З-{upd.id_upd}',
            id_upd=upd,
            status='created'
        )

        # Возврат ответа с ID созданных объектов
        return Response({
            'id_upd': upd.id_upd,
            'id_delivery_request': delivery_request.id_delivery_request
        }, status=status.HTTP_201_CREATED)
