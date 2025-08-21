"""Imports"""
from django.db import models

# Create your models here.
class User(models.Model):
    """User"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Order(models.Model):
    """Order per user"""
    order_id = models.AutoField(primary_key=True)
    details = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
