"""Imports from different libraries"""
import hashlib
import uuid
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer, CheckoutSerializer
from .pagination import OrderCursorPagination


def _hash_payload(payload):
    """Helper function to hash payload for idempotency"""
    return hashlib.sha256(str(payload).encode()).hexdigest()


class CheckoutView(APIView):
    """Checkout View"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Handling post requests"""
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        payload = serializer.validated_data
        raw_key = payload.get('idempotency_key')

        # Generate idempotency key if not provided
        if not raw_key:
            raw_key = str(uuid.uuid4())

        req_hash = _hash_payload(payload)
        currency = payload.get('currency', 'USD')

        # First, check if an order already exists for this (user, key)
        existing = Order.objects.filter(user=request.user, idempotency_key=raw_key).first()
        if existing:
            if existing.request_hash != req_hash:
                return Response({
                    'detail': 'Idempotency conflict: this key was used with a different payload.'
                }, status=status.HTTP_409_CONFLICT)
            data = OrderSerializer(existing).data
            return Response(data, status=status.HTTP_200_OK, headers={'Idempotency-Replayed': '1'})

        # Otherwise, attempt to create a new order atomically. If another request
        # races with the same key, the unique constraint will raise IntegrityError.
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    idempotency_key=raw_key,
                    request_hash=req_hash,
                    currency=currency,
                    status='paid', # minimal demo; in real systems, integrate payment first
                )

                total = 0
                items_to_create = []
                for it in payload['items']:
                    total += int(it['price_cents']) * int(it['quantity'])
                    items_to_create.append(OrderItem(order=order, **it))
                OrderItem.objects.bulk_create(items_to_create)

                order.total_cents = total
                order.save(update_fields=['total_cents'])

                data = OrderSerializer(order).data
                return Response(data, status=status.HTTP_201_CREATED, headers={'Idempotency-Replayed': '0'})
        except IntegrityError:
            # Another request created it first. Return that one if the hash matches; else 409.
            race = Order.objects.get(user=request.user, idempotency_key=raw_key)
            if race.request_hash != req_hash:
                return Response({
                    'detail': 'Idempotency conflict after race: key used with a different payload.'
                }, status=status.HTTP_409_CONFLICT)
            data = OrderSerializer(race).data
            return Response(data, status=status.HTTP_200_OK, headers={'Idempotency-Replayed': '1'})


from .serializers import OrderSerializer, CheckoutSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Order View Set"""
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    pagination_class = OrderCursorPagination

    def get_queryset(self):
        # Per-user isolation: users can only view their own orders
        return Order.objects.filter(user=self.request.user).order_by('-created_at').prefetch_related('items')


from rest_framework.generics import RetrieveAPIView

class OrderDetailView(RetrieveAPIView):
    """View a single order (detail)"""
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemDetailView(RetrieveAPIView):
    """View a single order item (detail)"""
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        # Only allow access to items belonging to the user's orders
        return OrderItem.objects.filter(order__user=self.request.user)
