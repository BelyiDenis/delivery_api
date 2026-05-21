"""
ViewSet приложения notifications (контроллеры в сиквенсах)

Реализованные сиквенсы:
№18 - Уведомление (создание) - POST /api/v1/notifications/
№19 - SOS (создание) - POST /api/v1/urgent-notifications/
"""

from .models import Log
from .serializers import LogSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Notification, UrgentNotification
from .serializers import NotificationSerializer, UrgentNotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Сиквенс №18: POST /api/v1/notifications/ - отправка уведомления о проблеме.
    Только для водителя.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 'driver':
            return Response({'error': 'Только водитель может отправлять уведомления'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)


class UrgentNotificationViewSet(viewsets.ModelViewSet):
    """
    Сиквенс №19: POST /api/v1/urgent-notifications/ - отправка SOS.
    Только для водителя.
    """
    queryset = UrgentNotification.objects.all()
    serializer_class = UrgentNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 'driver':
            return Response({'error': 'Только водитель может отправлять SOS'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)


class AdminLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Сиквенс №25: GET /api/v1/admin/logs/
    Просмотр логов системы (только для администратора).
    """
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Только администратор может смотреть логи
        if self.request.user.role != 'admin':
            return Log.objects.none()
        return Log.objects.all()

    def list(self, request, *args, **kwargs):
        """
        GET /api/v1/admin/logs/
        Поддерживает фильтрацию:
        - ?action=CREATE
        - ?model_name=DeliveryRequest
        - ?page=1&page_size=10
        """
        queryset = self.get_queryset()

        # Фильтрация по действию
        action_filter = request.query_params.get('action')
        if action_filter:
            queryset = queryset.filter(action=action_filter)

        # Фильтрация по модели
        model_filter = request.query_params.get('model_name')
        if model_filter:
            queryset = queryset.filter(model_name=model_filter)

        # Пагинация
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
