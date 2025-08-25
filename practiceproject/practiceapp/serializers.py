from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemInSerializer(serializers.Serializer):
    sku = serializers.CharField(max_length=64)
    name = serializers.CharField(max_length=200)
    price_cents = serializers.IntegerField(min_value=0)
    quantity = serializers.IntegerField(min_value=1)


class CheckoutSerializer(serializers.Serializer):
    items = OrderItemInSerializer(many=True)
    currency = serializers.CharField(max_length=3, default='USD')
    idempotency_key = serializers.CharField(max_length=64, required=False)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("sku", "name", "price_cents", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "currency", "total_cents", "status", "created_at", "items")