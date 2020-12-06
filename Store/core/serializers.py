from rest_framework import serializers

from .models import StoreOrder


class StoreOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreOrder
        fields = '__all__'
