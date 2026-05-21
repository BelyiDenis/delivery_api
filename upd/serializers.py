from rest_framework import serializers
from .models import UPD


class UPDSerializer(serializers.ModelSerializer):
    class Meta:
        model = UPD
        fields = '__all__'
