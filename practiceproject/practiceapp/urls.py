"""Imports and libraries"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import CheckoutView, OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('token/', obtain_auth_token, name='obtain-token'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
