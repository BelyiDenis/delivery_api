from rest_framework import serializers
from .models import Waybill, ClosedDeliveryRequest


class WaybillSerializer(serializers.ModelSerializer):
    """Сериализатор для путевого листа с дополнительными данными"""

    delivery_request_number = serializers.SerializerMethodField()
    driver_details = serializers.SerializerMethodField()
    vehicle_details = serializers.SerializerMethodField()
    route_details = serializers.SerializerMethodField()

    class Meta:
        model = Waybill
        fields = '__all__'

    def get_delivery_request_number(self, obj):
        return obj.id_delivery_request.number_delivery_request

    def get_driver_details(self, obj):
        return {
            'full_name': f'{obj.id_driver.id_user.last_name} {obj.id_driver.id_user.first_name}',
            'driver_license_number': obj.id_driver.driver_license_number,
        }

    def get_vehicle_details(self, obj):
        return {
            'license_plate': obj.vehicle_license_plate.license_plate,
            'vehicle_type': obj.vehicle_license_plate.vehicle_type,
        }

    def get_route_details(self, obj):
        return {
            'loading_address_warehouse': obj.id_route.loading_address_warehouse,
            'unloading_address_client': obj.id_route.unloading_address_client,
            'distance_km': obj.id_route.distance_km,
            'planned_duration_minutes': obj.id_route.planned_duration_minutes,
        }


class ClosedDeliveryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosedDeliveryRequest
        fields = '__all__'
