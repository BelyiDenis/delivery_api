"""
Модели приложения waybills: путевой лист и архив закрытых заявок

Соответствует инфологической модели: таблицы Путевой лист и Закрытая заявка
"""

from django.db import models
from delivery_requests.models import DeliveryRequest
from users.models import Driver
from vehicles.models import Vehicle
from routes.models import Route


class Waybill(models.Model):
    """
    Путевой лист для водителя.
    Формируется после погрузки товара.
    """

    STATUS_CHOICES = [
        ('formed', 'Сформирован'),
        ('transferred', 'Передан водителю'),
    ]

    id_waybill = models.AutoField(primary_key=True)
    number_waybill = models.CharField(
        max_length=20, unique=True)  # Уникальный номер
    id_delivery_request = models.OneToOneField(
        DeliveryRequest, on_delete=models.CASCADE, db_column='id_delivery_request')
    id_driver = models.ForeignKey(
        Driver, on_delete=models.RESTRICT, db_column='id_driver')
    vehicle_license_plate = models.ForeignKey(
        Vehicle, on_delete=models.RESTRICT, db_column='vehicle_license_plate', to_field='license_plate')
    id_route = models.ForeignKey(
        Route, on_delete=models.RESTRICT, db_column='id_route')
    issue_date = models.DateTimeField(auto_now_add=True)  # Дата выдачи
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='formed')

    class Meta:
        db_table = 'waybill'

    def __str__(self):
        return f'Путевой лист {self.number_waybill}'


class ClosedDeliveryRequest(models.Model):
    """
    Архив закрытых заявок.
    Хранит полную копию заявки в формате JSON.
    """

    id_closed_request = models.AutoField(primary_key=True)
    id_delivery_request = models.IntegerField(
        unique=True)  # ID исходной заявки
    full_request_copy_json = models.TextField()  # JSON-копия заявки
    delivery_report_json = models.TextField(
        blank=True, null=True)  # Отчёт о доставке
    closing_date = models.DateTimeField(auto_now_add=True)  # Дата архивации

    class Meta:
        db_table = 'closed_delivery_request'

    def __str__(self):
        return f'Архив заявки {self.id_delivery_request}'
