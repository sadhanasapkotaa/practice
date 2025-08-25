from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Order, OrderItem


User = get_user_model()

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_order(self):
        order = Order.objects.create(
            user=self.user,
            idempotency_key='idemkey1',
            request_hash='hash1',
            total_cents=1000,
            currency='USD',
            status='paid',
        )
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_cents, 1000)
        self.assertEqual(order.currency, 'USD')
        self.assertEqual(order.status, 'paid')
        self.assertEqual(str(order), f"Order {order.id} by {self.user}")

    def test_unique_idempotency_key_per_user(self):
        Order.objects.create(
            user=self.user,
            idempotency_key='unique-key',
            request_hash='hash1',
        )
        with self.assertRaises(Exception):
            Order.objects.create(
                user=self.user,
                idempotency_key='unique-key',
                request_hash='hash2',
            )


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='itemuser', password='testpass')
        self.order = Order.objects.create(
            user=self.user,
            idempotency_key='itemkey',
            request_hash='hash',
        )

    def test_create_order_item(self):
        item = OrderItem.objects.create(
            order=self.order,
            sku='SKU123',
            name='Test Product',
            price_cents=500,
            quantity=2,
        )
        self.assertEqual(item.line_total_cents(), 1000)
        self.assertEqual(str(item), 'SKU123 x2')
		self.assertEqual(str(item), 'SKU123 x2')
