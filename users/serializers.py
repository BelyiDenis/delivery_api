"""
Сериализаторы приложения users (граничный класс в сиквенсах)
"""

from rest_framework import serializers
from .models import User, Driver


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'middle_name',
                  'role', 'phone', 'email', 'is_active')


class DriverSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Driver с добавлением данных пользователя"""
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = '__all__'

    def get_user_details(self, obj):
        """Получение данных пользователя, связанного с водителем"""
        return {
            'id': obj.id_user.id,
            'last_name': obj.id_user.last_name,
            'first_name': obj.id_user.first_name,
            'phone': obj.id_user.phone,
        }
