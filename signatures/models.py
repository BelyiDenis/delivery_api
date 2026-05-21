from django.db import models
from delivery_requests.models import DeliveryRequest


class ElectronicSignature(models.Model):
    SIGNER_CHOICES = [('driver', 'Водитель'), ('client', 'Клиент')]
    STATUS_CHOICES = [('success', 'Успешно'), ('error', 'Ошибка')]

    id_signature = models.AutoField(primary_key=True)
    id_delivery_request = models.ForeignKey(
        DeliveryRequest, on_delete=models.CASCADE, db_column='id_delivery_request')
    signer_type = models.CharField(max_length=20, choices=SIGNER_CHOICES)
    signature_body = models.TextField()
    signature_datetime = models.DateTimeField(auto_now_add=True)
    verification_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='success')

    class Meta:
        db_table = 'electronic_signature'
        unique_together = ['id_delivery_request', 'signer_type']
