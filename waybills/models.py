from django.db import models
from delivery_requests.models import DeliveryRequest
from users.models import Driver
from vehicles.models import Vehicle
from routes.models import Route


class Waybill(models.Model):
    STATUS_CHOICES = [
        ('formed', 'Сформирован'),
        ('transferred', 'Передан водителю'),
    ]

    id_waybill = models.AutoField(primary_key=True)
    number_waybill = models.CharField(max_length=20, unique=True)
    id_delivery_request = models.OneToOneField(
        DeliveryRequest, on_delete=models.CASCADE, db_column='id_delivery_request')
    id_driver = models.ForeignKey(
        Driver, on_delete=models.RESTRICT, db_column='id_driver')
    vehicle_license_plate = models.ForeignKey(
        Vehicle, on_delete=models.RESTRICT, db_column='vehicle_license_plate', to_field='license_plate')
    id_route = models.ForeignKey(
        Route, on_delete=models.RESTRICT, db_column='id_route')
    issue_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='formed')

    class Meta:
        db_table = 'waybill'

    def __str__(self):
        return f'Путевой лист {self.number_waybill}'


class ClosedDeliveryRequest(models.Model):
    id_closed_request = models.AutoField(primary_key=True)
    id_delivery_request = models.IntegerField(unique=True)
    full_request_copy_json = models.TextField()
    delivery_report_json = models.TextField(blank=True, null=True)
    closing_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'closed_delivery_request'

    def __str__(self):
        return f'Архив заявки {self.id_delivery_request}'
