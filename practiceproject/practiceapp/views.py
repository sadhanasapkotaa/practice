from django.shortcuts import render

# Create your views here.

from .models import User, Order
from .serializers import UserSerializer, OrderSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

def student_view(self):
    """Student View"""
    query_data = User.objects.all()
    serialized_data = UserSerializer(query_data, many = True)
    json_data = JSONRenderer().render(serialized_data.data)

    return Response(json_data, content_type='application/json')

def order_view(self):
    """Order View"""
    query_data = Order.objects.all()
    serialized_data = OrderSerializer(query_data, many = True)
    json_data = JSONRenderer().render(serialized_data.data)

    return Response(json_data, content_type='application/json')

