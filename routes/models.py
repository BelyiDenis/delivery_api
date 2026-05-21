"""
Модель приложения routes: маршрут доставки

Соответствует инфологической модели: таблица Маршрут
"""

from django.db import models


class Route(models.Model):
    """
    Маршрут доставки от склада до клиента.
    """

    id_route = models.AutoField(primary_key=True)
    loading_address_warehouse = models.CharField(
        max_length=500)  # Адрес склада
    unloading_address_client = models.CharField(
        max_length=500)  # Адрес клиента
    distance_km = models.DecimalField(
        max_digits=8, decimal_places=2)  # Расстояние в км
    planned_duration_minutes = models.IntegerField()  # Плановая длительность

    class Meta:
        db_table = 'route'

    def __str__(self):
        return f'{self.loading_address_warehouse} -> {self.unloading_address_client}'
