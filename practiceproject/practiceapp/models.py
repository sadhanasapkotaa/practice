"""UUID and django default user model import"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Order(models.Model):
    """Order model representing a user's order."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    idempotency_key = models.CharField(max_length=64)
    request_hash = models.CharField(max_length=64)
    total_cents = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, default='paid')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "idempotency_key"], name="uniq_user_idempo"),
        ]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["user", "idempotency_key"]),
        ]

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class OrderItem(models.Model):
    """Order Item Details"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    sku = models.CharField(max_length=64)
    name = models.CharField(max_length=200)
    price_cents = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def line_total_cents(self) -> int:
        return self.price_cents * self.quantity

    def __str__(self):
        return f"{self.sku} x{self.quantity}"