from .models import Log
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


class LogSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Log
        fields = '__all__'

    def get_user_details(self, obj):
        if obj.user:
            return {
                'id': obj.user.id,
                'last_name': obj.user.last_name,
                'first_name': obj.user.first_name,
                'phone': obj.user.phone,
            }
        return None
