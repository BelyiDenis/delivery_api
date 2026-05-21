from django.contrib import admin
from .models import Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id_route', 'loading_address_warehouse',
                    'unloading_address_client', 'distance_km')
    search_fields = ('loading_address_warehouse', 'unloading_address_client')
