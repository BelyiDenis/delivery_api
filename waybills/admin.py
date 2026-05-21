from django.contrib import admin
from .models import Waybill, ClosedDeliveryRequest

@admin.register(Waybill)
class WaybillAdmin(admin.ModelAdmin):
    list_display = ('id_waybill', 'number_waybill', 'id_delivery_request', 'issue_date', 'status')
    list_filter = ('status',)
    search_fields = ('number_waybill',)

@admin.register(ClosedDeliveryRequest)
class ClosedDeliveryRequestAdmin(admin.ModelAdmin):
    list_display = ('id_closed_request', 'id_delivery_request', 'closing_date')
