from django.contrib import admin
from .models import Notification, UrgentNotification, Log


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id_notification', 'id_delivery_request',
                    'problem_type', 'status', 'notification_datetime')
    list_filter = ('problem_type', 'status')
    search_fields = ('driver_comment',)


@admin.register(UrgentNotification)
class UrgentNotificationAdmin(admin.ModelAdmin):
    list_display = ('id_sos', 'id_delivery_request', 'status', 'sos_datetime')
    list_filter = ('status',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    """
    Админка для просмотра логов (Сиквенс №25)
    """
    list_display = ('created_at', 'user', 'action',
                    'model_name', 'object_id', 'ip_address')
    list_filter = ('action', 'model_name', 'created_at')
    search_fields = ('user__phone', 'user__last_name',
                     'model_name', 'object_id')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'action', 'model_name', 'object_id')
        }),
        ('Детали изменения', {
            'fields': ('old_value', 'new_value'),
            'classes': ('collapse',)
        }),
        ('Техническая информация', {
            'fields': ('ip_address', 'created_at')
        }),
    )
