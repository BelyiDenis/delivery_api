"""
Сериализатор приложения delivery_requests (граничный класс в сиквенсах)
"""

from rest_framework import serializers
from .models import DeliveryRequest


class DeliveryRequestSerializer(serializers.ModelSerializer):
    """Сериализатор для модели DeliveryRequest с дополнительными полями"""

    upd_details = serializers.SerializerMethodField()
    driver_details = serializers.SerializerMethodField()
    vehicle_details = serializers.SerializerMethodField()

    class Meta:
        model = DeliveryRequest
        fields = '__all__'

    def get_upd_details(self, obj):
        """Получение данных из связанного УПД"""
        if obj.id_upd:
            return {
                'number_upd': obj.id_upd.number_upd,
                'client_name': obj.id_upd.client_name,
                'client_delivery_address': obj.id_upd.client_delivery_address,
                'product_name': obj.id_upd.product_name,
                'product_volume_m3': obj.id_upd.product_volume_m3,
                'product_price_rub': obj.id_upd.product_price_rub,
            }
        return None

    def get_driver_details(self, obj):
        """Получение данных о водителе"""
        if obj.id_driver:
            return {
                'id_driver': obj.id_driver.id_driver,
                'full_name': f'{obj.id_driver.id_user.last_name} {obj.id_driver.id_user.first_name}',
                'phone': obj.id_driver.id_user.phone,
            }
        return None

    def get_vehicle_details(self, obj):
        """Получение данных о транспортном средстве"""
        if obj.vehicle_license_plate:
            return {
                'license_plate': obj.vehicle_license_plate.license_plate,
                'vehicle_type': obj.vehicle_license_plate.vehicle_type,
                'capacity_tons': obj.vehicle_license_plate.capacity_tons,
            }
        return None
