from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'vehicle_type', 'capacity_tons', 'status')
    list_filter = ('vehicle_type', 'status')
    search_fields = ('license_plate',)
