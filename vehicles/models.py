"""
Модель приложения vehicles: транспортное средство

Соответствует инфологической модели: таблица Транспортное средство
"""

from django.db import models


class Vehicle(models.Model):
    """
    Транспортное средство для доставки.
    """

    TYPE_CHOICES = [
        ('gazel', 'Газель'),
        ('foton', 'Фотон'),
        ('long', 'Длинномер'),
    ]
    STATUS_CHOICES = [
        ('free', 'Свободен'),
        ('busy', 'Занят'),
    ]

    license_plate = models.CharField(
        max_length=20, primary_key=True)  # Госномер (PK)
    vehicle_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    capacity_tons = models.DecimalField(
        max_digits=10, decimal_places=2)  # Грузоподъёмность
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='free')

    class Meta:
        db_table = 'vehicle'

    def __str__(self):
        return self.license_plate
