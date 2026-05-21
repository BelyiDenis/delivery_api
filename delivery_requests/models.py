"""
Модель приложения delivery_requests: заявка на доставку
Соответствует инфологической модели: таблица Заявка на доставку
"""

from django.db import models
from upd.models import UPD
from users.models import Driver
from vehicles.models import Vehicle


class DeliveryRequest(models.Model):
    """
    Заявка на доставку пиломатериалов.
    Основной документ, сопровождающий весь процесс.
    """

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('driver_assigned', 'Назначен водитель'),
        ('in_transit', 'В пути'),
        ('signed', 'Подписана'),
        ('completed', 'Выполнена'),
    ]

    id_delivery_request = models.AutoField(primary_key=True)
    number_delivery_request = models.CharField(max_length=20, unique=True)
    id_upd = models.ForeignKey(
        UPD, on_delete=models.RESTRICT, db_column='id_upd')
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='created')
    id_driver = models.ForeignKey(
        Driver, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_driver')
    vehicle_license_plate = models.ForeignKey(
        Vehicle, on_delete=models.SET_NULL, null=True, blank=True, db_column='vehicle_license_plate', to_field='license_plate')
    loading_date = models.DateTimeField(null=True, blank=True)
    arrival_to_client_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'delivery_request'

    def __str__(self):
        return f'Заявка {self.number_delivery_request}'
