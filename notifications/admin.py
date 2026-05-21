from django.contrib import admin
from .models import Notification, UrgentNotification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id_notification', 'id_delivery_request',
                    'problem_type', 'status', 'notification_datetime')
    list_filter = ('problem_type', 'status')


@admin.register(UrgentNotification)
class UrgentNotificationAdmin(admin.ModelAdmin):
    list_display = ('id_sos', 'id_delivery_request', 'status', 'sos_datetime')
    list_filter = ('status',)
