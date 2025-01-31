import uuid
from rest_framework import serializers
from .models import Customer, Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['__all__']
        
    def update(self, instance, validated_data):
        if not instance.code:
            instance.code = 'CUST' + str(uuid.uuid4().int)[:6]
        return super().update(instance, validated_data)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'item', 'amount', 'time', ]
