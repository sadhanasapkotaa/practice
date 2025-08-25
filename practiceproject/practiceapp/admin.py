# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem
import hashlib, json
from django.utils.crypto import get_random_string

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "currency", "total_cents", "created_at")
    list_filter = ("status", "currency", "created_at")
    search_fields = ("id", "user__username")
    readonly_fields = ("request_hash", "total_cents", "created_at")
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        if not obj.idempotency_key:
            obj.idempotency_key = f"admin-{get_random_string(12)}"
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        total = sum(i.price_cents * i.quantity for i in obj.items.all())
        items = list(obj.items.values("sku", "name", "price_cents", "quantity"))
        payload = {"items": items, "currency": obj.currency}
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        obj.total_cents = total
        obj.request_hash = hashlib.sha256(canonical.encode()).hexdigest()
        obj.save(update_fields=["total_cents", "request_hash"])

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "sku", "name", "price_cents", "quantity")
    search_fields = ("sku", "name", "order__id")
    list_filter = ("order",)
