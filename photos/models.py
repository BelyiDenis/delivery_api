from django.db import models
from delivery_requests.models import DeliveryRequest


class ProductPhoto(models.Model):
    id_photo = models.AutoField(primary_key=True)
    id_delivery_request = models.ForeignKey(
        DeliveryRequest, on_delete=models.CASCADE, db_column='id_delivery_request')
    photo_file_path = models.CharField(max_length=500)
    upload_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_photo'
