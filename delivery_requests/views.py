"""
ViewSet приложения delivery_requests (контроллеры в сиквенсах)

Реализованные сиквенсы:
№3 - Заявки (список) - GET /api/v1/delivery-requests/
№4 - Заявка (создание) - POST /api/v1/delivery-requests/
№5 - Заявка (детали) - GET /api/v1/delivery-requests/{id}/
№6 - Заявка (обновление) - PATCH /api/v1/delivery-requests/{id}/
№7 - Заявка (назначение водителя) - PATCH /api/v1/delivery-requests/{id}/assign-driver/
№8 - Заявка (закрытие) - POST /api/v1/delivery-requests/{id}/close/
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import DeliveryRequest
from .serializers import DeliveryRequestSerializer
from upd.models import UPD


class DeliveryRequestViewSet(viewsets.ModelViewSet):
    queryset = DeliveryRequest.objects.all()
    serializer_class = DeliveryRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Сиквенс №3: получение списка заявок с фильтрацией по роли.
        Водитель видит только свои заявки.
        Диспетчер, менеджер, администратор видят все.
        """
        user = self.request.user
        if user.role == 'driver':
            return DeliveryRequest.objects.filter(id_driver__id_user=user)
        return DeliveryRequest.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Сиквенс №4: создание заявки на основе УПД.
        """
        id_upd = request.data.get('id_upd')
        if not id_upd:
            return Response({'error': 'id_upd required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            upd = UPD.objects.get(id_upd=id_upd)
        except UPD.DoesNotExist:
            return Response({'error': 'UPD not found'}, status=status.HTTP_404_NOT_FOUND)

        delivery_request = DeliveryRequest.objects.create(
            number_delivery_request=f'З-{upd.id_upd}',
            id_upd=upd,
            status='created'
        )
        serializer = self.get_serializer(delivery_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='assign-driver')
    def assign_driver(self, request, pk=None):
        """
        Сиквенс №7: назначение водителя на заявку (только для диспетчера).
        """
        if request.user.role != 'dispatcher':
            return Response({'error': 'Только диспетчер может назначать водителя'},
                            status=status.HTTP_403_FORBIDDEN)

        delivery = self.get_object()
        driver_id = request.data.get('id_driver')
        license_plate = request.data.get('vehicle_license_plate')

        if not driver_id or not license_plate:
            return Response({'error': 'id_driver и vehicle_license_plate обязательны'},
                            status=status.HTTP_400_BAD_REQUEST)

        delivery.id_driver_id = driver_id
        delivery.vehicle_license_plate_id = license_plate
        delivery.status = 'driver_assigned'
        delivery.save()

        serializer = self.get_serializer(delivery)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='close')
    def close(self, request, pk=None):
        """
        Сиквенс №8: закрытие заявки (только для диспетчера).
        Проверяет наличие подписей и фото перед закрытием.
        """
        if request.user.role != 'dispatcher':
            return Response({'error': 'Только диспетчер может закрывать заявки'},
                            status=status.HTTP_403_FORBIDDEN)

        delivery = self.get_object()

        # Проверка наличия подписей
        from signatures.models import ElectronicSignature
        has_driver_sig = ElectronicSignature.objects.filter(
            id_delivery_request=delivery, signer_type='driver', verification_status='success'
        ).exists()
        has_client_sig = ElectronicSignature.objects.filter(
            id_delivery_request=delivery, signer_type='client', verification_status='success'
        ).exists()

        if not has_driver_sig or not has_client_sig:
            return Response({'error': 'Отсутствует подпись клиента'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверка наличия фото
        from photos.models import ProductPhoto
        if not ProductPhoto.objects.filter(id_delivery_request=delivery).exists():
            return Response({'error': 'Отсутствуют фото груза'},
                            status=status.HTTP_400_BAD_REQUEST)

        delivery.status = 'completed'
        delivery.save()

        # Сохранение в архив
        from waybills.models import ClosedDeliveryRequest
        ClosedDeliveryRequest.objects.create(
            id_delivery_request=delivery.id_delivery_request,
            full_request_copy_json='{}'
        )

        return Response({'message': 'Заявка закрыта', 'status': 'completed'})
