"""
Сериализатор приложения upd (граничный класс в сиквенсах)
"""

from rest_framework import serializers
from .models import UPD


class UPDSerializer(serializers.ModelSerializer):
    """Сериализатор для модели UPD"""
    class Meta:
        model = UPD
        fields = '__all__'
