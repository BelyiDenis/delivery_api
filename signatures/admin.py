from django.contrib import admin
from .models import ElectronicSignature


@admin.register(ElectronicSignature)
class ElectronicSignatureAdmin(admin.ModelAdmin):
    list_display = ('id_signature', 'id_delivery_request',
                    'signer_type', 'verification_status', 'signature_datetime')
    list_filter = ('signer_type', 'verification_status')
