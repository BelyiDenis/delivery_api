from django.db import models
from delivery_requests.models import DeliveryRequest


class Notification(models.Model):
    PROBLEM_CHOICES = [
        ('delay', 'Задержка'),
        ('breakdown', 'Поломка'),
        ('client_refusal', 'Отказ клиента'),
        ('other', 'Другое'),
    ]
    STATUS_CHOICES = [
        ('new', 'Новое'),
        ('read', 'Прочитано'),
    ]

    id_notification = models.AutoField(primary_key=True)
    id_delivery_request = models.ForeignKey(
        DeliveryRequest, on_delete=models.CASCADE, db_column='id_delivery_request')
    problem_type = models.CharField(max_length=50, choices=PROBLEM_CHOICES)
    driver_comment = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='new')
    notification_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification'


class UrgentNotification(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Отправлено'),
        ('processed', 'Обработано'),
    ]

    id_sos = models.AutoField(primary_key=True)
    id_delivery_request = models.ForeignKey(
        DeliveryRequest, on_delete=models.CASCADE, db_column='id_delivery_request')
    sos_comment = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='sent')
    sos_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'urgent_notification'


class Log(models.Model):
    """
    Модель для логирования действий пользователей в системе.
    Соответствует Сиквенсу №25 - Логи (просмотр)
    """

    ACTION_CHOICES = [
        ('CREATE', 'Создание'),
        ('UPDATE', 'Обновление'),
        ('DELETE', 'Удаление'),
        ('LOGIN', 'Вход'),
        ('LOGOUT', 'Выход'),
    ]

    id_log = models.AutoField(primary_key=True, verbose_name='ID лога')
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL,
                             null=True, blank=True, verbose_name='Пользователь')
    action = models.CharField(
        max_length=20, choices=ACTION_CHOICES, verbose_name='Действие')
    model_name = models.CharField(max_length=100, verbose_name='Модель')
    object_id = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='ID объекта')
    old_value = models.TextField(
        blank=True, null=True, verbose_name='Старое значение')
    new_value = models.TextField(
        blank=True, null=True, verbose_name='Новое значение')
    ip_address = models.GenericIPAddressField(
        blank=True, null=True, verbose_name='IP адрес')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата и время')

    class Meta:
        db_table = 'log'
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.created_at} - {self.user} - {self.action} - {self.model_name}'
