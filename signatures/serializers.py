from rest_framework import serializers
from .models import ElectronicSignature


class ElectronicSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicSignature
        fields = '__all__'
