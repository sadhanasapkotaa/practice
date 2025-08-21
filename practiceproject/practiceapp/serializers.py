"""Importing Serializers"""
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""
    id = serializers.IntegerField()
    name = serializers.CharField(max_length = 100)
    address = serializers.CharField(max_length = 200)


class OrderSerializer(serializers.ModelSerializer):
    """Order Serializer"""
    order_id = serializers.IntegerField()
    details = serializers.CharField(max_length = 300)
    