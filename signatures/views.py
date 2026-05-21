"""
ViewSet приложения signatures (контроллеры в сиквенсах)

Реализованные сиквенсы:
№16 - Подпись (создание) - POST /api/v1/electronic-signatures/
№17 - Подпись (статус по заявке) - GET /api/v1/delivery-requests/{id}/signatures/
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ElectronicSignature
from .serializers import ElectronicSignatureSerializer
from delivery_requests.models import DeliveryRequest


class ElectronicSignatureViewSet(viewsets.ModelViewSet):
    queryset = ElectronicSignature.objects.all()
    serializer_class = ElectronicSignatureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Сиквенс №16: создание электронной подписи (только для водителя).
        """
        if request.user.role != 'driver':
            return Response({'error': 'Только водитель может создавать подписи'},
                            status=status.HTTP_403_FORBIDDEN)

        request_id = request.data.get('id_delivery_request')
        signer_type = request.data.get('signer_type')

        if ElectronicSignature.objects.filter(
            id_delivery_request_id=request_id, signer_type=signer_type
        ).exists():
            return Response({'error': 'Подпись уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Если оба подписали → меняем статус заявки
        if ElectronicSignature.objects.filter(id_delivery_request_id=request_id).count() == 2:
            DeliveryRequest.objects.filter(
                id_delivery_request=request_id).update(status='signed')

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='by-request/(?P<request_id>[^/.]+)')
    def by_request(self, request, request_id=None):
        """
        Сиквенс №17: получение статуса подписей по заявке.
        """
        signatures = ElectronicSignature.objects.filter(
            id_delivery_request_id=request_id)
        serializer = self.get_serializer(signatures, many=True)
        return Response(serializer.data)
