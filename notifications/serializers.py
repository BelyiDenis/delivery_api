from rest_framework import serializers
from .models import Notification, UrgentNotification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class UrgentNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrgentNotification
        fields = '__all__'
