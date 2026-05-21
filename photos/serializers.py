from rest_framework import serializers
from .models import ProductPhoto


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = '__all__'
