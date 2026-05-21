"""
ViewSet приложения notifications (контроллеры в сиквенсах)

Реализованные сиквенсы:
№18 - Уведомление (создание) - POST /api/v1/notifications/
№19 - SOS (создание) - POST /api/v1/urgent-notifications/
"""

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
