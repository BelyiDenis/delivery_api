from django.contrib import admin
from .models import ProductPhoto


@admin.register(ProductPhoto)
class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ('id_photo', 'id_delivery_request', 'upload_datetime')
    search_fields = ('id_delivery_request__number_delivery_request',)
