"""
ViewSet приложения photos (контроллеры в сиквенсах)

Реализованные сиквенсы:
№14 - Фото (загрузка) - POST /api/v1/product-photos/
№15 - Фото (по заявке) - GET /api/v1/delivery-requests/{id}/photos/
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import ProductPhoto
from .serializers import ProductPhotoSerializer
from delivery_requests.models import DeliveryRequest


class ProductPhotoViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с фото товара.
    """
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Сиквенс №14: загрузка фото груза (только для водителя).
        """
        # Проверка прав доступа
        if request.user.role != 'driver':
            return Response({'error': 'Только водитель может загружать фото'},
                            status=status.HTTP_403_FORBIDDEN)

        photo_file = request.FILES.get('photo_file')
        request_id = request.data.get('id_delivery_request')

        if not photo_file or not request_id:
            return Response({'error': 'photo_file и id_delivery_request обязательны'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Сохранение файла на сервере
        file_path = default_storage.save(
            f'photos/request_{request_id}_{photo_file.name}',
            ContentFile(photo_file.read())
        )

        # Создание записи в БД
        photo = ProductPhoto.objects.create(
            id_delivery_request_id=request_id,
            photo_file_path=file_path
        )

        return Response({
            'id_photo': photo.id_photo,
            'photo_url': default_storage.url(file_path),
            'upload_datetime': photo.upload_datetime
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='by-request/(?P<request_id>[^/.]+)')
    def by_request(self, request, request_id=None):
        """
        Сиквенс №15: получение всех фото по заявке.
        """
        photos = ProductPhoto.objects.filter(id_delivery_request_id=request_id)
        serializer = self.get_serializer(photos, many=True)
        return Response(serializer.data)
