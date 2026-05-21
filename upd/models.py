"""
Модель приложения upd: УПД (универсальный передаточный документ)
Соответствует инфологической модели: таблица УПД
"""

from django.db import models


class UPD(models.Model):
    """
    Универсальный передаточный документ из учётной системы (1С).
    Приходит уже готовым, содержит все данные о заказе.
    """

    STATUS_CHOICES = [
        ('received', 'Получен'),
        ('error', 'Ошибка'),
    ]

    id_upd = models.AutoField(primary_key=True)
    number_upd = models.CharField(max_length=50, unique=True)
    client_name = models.CharField(max_length=255)
    client_delivery_address = models.CharField(max_length=500)
    product_name = models.CharField(max_length=255)
    product_volume_m3 = models.DecimalField(max_digits=10, decimal_places=2)
    product_price_rub = models.DecimalField(max_digits=15, decimal_places=2)
    wood_documents_link = models.CharField(
        max_length=500, blank=True, null=True)
    status_upd = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='received')
    received_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'upd'

    def __str__(self):
        return f'{self.number_upd} - {self.client_name}'
