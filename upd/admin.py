from django.contrib import admin
from .models import UPD

@admin.register(UPD)
class UPDAdmin(admin.ModelAdmin):
    list_display = ('id_upd', 'number_upd', 'client_name', 'product_name', 'status_upd', 'received_datetime')
    list_filter = ('status_upd',)
    search_fields = ('number_upd', 'client_name')
