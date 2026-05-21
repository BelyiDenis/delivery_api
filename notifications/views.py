from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Notification, UrgentNotification
from .serializers import NotificationSerializer, UrgentNotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if request.user.role != 'driver':
            return Response({'error': 'Only driver can send notifications'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class UrgentNotificationViewSet(viewsets.ModelViewSet):
    queryset = UrgentNotification.objects.all()
    serializer_class = UrgentNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        if request.user.role != 'driver':
            return Response({'error': 'Only driver can send SOS'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)
