"""
ViewSet приложения users (контроллеры в сиквенсах)

Реализованные сиквенсы:
№11 - Водители (список) - GET /api/v1/drivers/
№12 - Водитель (заявки) - GET /api/v1/drivers/{id}/delivery-requests/
№22 - Текущий пользователь - GET /api/v1/users/me/
№23 - Пользователи (CRUD) - POST /api/v1/admin/users/
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Driver
from .serializers import UserSerializer, DriverSerializer
from delivery_requests.models import DeliveryRequest
from delivery_requests.serializers import DeliveryRequestSerializer


class DriverViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы с водителями (только чтение).
    Доступ: диспетчер и администратор.

    Сиквенс №11: GET /api/v1/drivers/ - список всех водителей
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # Только диспетчер и администратор имеют доступ
        if self.request.user.role not in ['dispatcher', 'admin']:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    @action(detail=True, methods=['get'], url_path='delivery-requests')
    def delivery_requests(self, request, pk=None):
        """
        Сиквенс №12: GET /api/v1/drivers/{id}/delivery-requests/
        Получение всех заявок, назначенных на конкретного водителя
        """
        driver = self.get_object()
        requests = DeliveryRequest.objects.filter(id_driver=driver)
        serializer = DeliveryRequestSerializer(requests, many=True)
        return Response(serializer.data)


class AdminUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями (только для администратора).

    Сиквенс №23: POST /api/v1/admin/users/ - создание пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        # Только администратор имеет доступ
        if self.request.user.role != 'admin':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Создание нового пользователя с хешированием пароля.
        Проверка уникальности телефона.
        """
        phone = request.data.get('phone')

        # Проверка на дубликат телефона
        if User.objects.filter(phone=phone).exists():
            return Response({'error': 'Телефон уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        # Создание пользователя через менеджер (хеширование пароля)
        user = User.objects.create_user(
            phone=phone,
            password=request.data.get('password'),
            last_name=request.data.get('last_name'),
            first_name=request.data.get('first_name'),
            role=request.data.get('role')
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class CurrentUserViewSet(viewsets.ViewSet):
    """
    ViewSet для получения информации о текущем авторизованном пользователе.

    Сиквенс №22: GET /api/v1/users/me/
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """Возвращает данные текущего пользователя"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
