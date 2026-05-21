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
