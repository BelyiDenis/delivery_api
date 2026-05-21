"""
ViewSet приложения waybills (контроллеры в сиквенсах)

Реализованные сиквенсы:
№9 - Путевой лист (формирование) - POST /api/v1/waybills/generate/
№10 - Путевой лист (по заявке) - GET /api/v1/waybills/by-request/{id}/
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Waybill
from .serializers import WaybillSerializer
from delivery_requests.models import DeliveryRequest
from routes.models import Route


class WaybillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Сиквенс №10: GET /api/v1/waybills/by-request/{id}/
    Получение путевого листа по ID заявки.
    """
    queryset = Waybill.objects.all()
    serializer_class = WaybillSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='by-request/(?P<request_id>[^/.]+)')
    def by_request(self, request, request_id=None):
        try:
            waybill = Waybill.objects.get(id_delivery_request_id=request_id)
            serializer = self.get_serializer(waybill)
            return Response(serializer.data)
        except Waybill.DoesNotExist:
            return Response({'error': 'Путевой лист не найден'}, status=status.HTTP_404_NOT_FOUND)


class WaybillGenerateViewSet(viewsets.ViewSet):
    """
    Сиквенс №9: POST /api/v1/waybills/generate/
    Формирование путевого листа (только для менеджера).
    """
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        if request.user.role != 'manager':
            return Response({'error': 'Только менеджер может формировать путевые листы'},
                            status=status.HTTP_403_FORBIDDEN)

        request_id = request.data.get('id_delivery_request')
        if not request_id:
            return Response({'error': 'id_delivery_request обязателен'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            delivery = DeliveryRequest.objects.get(
                id_delivery_request=request_id)
        except DeliveryRequest.DoesNotExist:
            return Response({'error': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)

        if not delivery.id_driver:
            return Response({'error': 'Водитель не назначен'}, status=status.HTTP_400_BAD_REQUEST)
        if not delivery.vehicle_license_plate:
            return Response({'error': 'Транспортное средство не назначено'}, status=status.HTTP_400_BAD_REQUEST)

        route = Route.objects.first()
        if not route:
            return Response({'error': 'Маршрут не найден'}, status=status.HTTP_400_BAD_REQUEST)

        waybill = Waybill.objects.create(
            number_waybill=f'ПЛ-{delivery.id_delivery_request}',
            id_delivery_request=delivery,
            id_driver=delivery.id_driver,
            vehicle_license_plate=delivery.vehicle_license_plate,
            id_route=route
        )

        serializer = WaybillSerializer(waybill)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
