from django.contrib import admin
from .models import DeliveryRequest


@admin.register(DeliveryRequest)
class DeliveryRequestAdmin(admin.ModelAdmin):
    list_display = ('id_delivery_request', 'number_delivery_request',
                    'status', 'loading_date', 'arrival_to_client_date')
    list_filter = ('status',)
    search_fields = ('number_delivery_request',)
    raw_id_fields = ('id_upd', 'id_driver', 'vehicle_license_plate')
