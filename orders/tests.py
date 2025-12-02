from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Order
from django.utils import timezone


class OrderHistoryViewTestCase(TestCase):
    

    def setUp(self):
       
        User = get_user_model()

        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com',
            address="123 Main St"
        )

        self.order1 = Order.objects.create(
            user=self.user, order_date=timezone.now(), total_amount=100.00
        )
        self.order2 = Order.objects.create(
            user=self.user, order_date=timezone.now() - timezone.timedelta(days=1), total_amount=200.00
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='password456',
            email='otheruser@example.com',
            address="456 Another St"
        )

    def test_order_history_view_authenticated(self):
        
        self.client.force_login(self.user)

        response = self.client.get(reverse('Orders:order_history'))

        self.assertEqual(response.status_code, 200)

        orders = response.context['orders']

        self.assertEqual(orders[0], self.order1)
        self.assertEqual(orders[1], self.order2)

        self.assertContains(response, str(self.order1.total_amount))
        self.assertContains(response, str(self.order2.total_amount))

    def test_order_history_view_other_user(self):
       
        self.client.force_login(self.other_user)

        response = self.client.get(reverse('Orders:order_history'))

        self.assertNotContains(response, str(self.order1.total_amount))
        self.assertNotContains(response, str(self.order2.total_amount))


class OrderDetailViewTestCase(TestCase):
    

    def setUp(self):
        
        User = get_user_model()

        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            email='testuser@example.com',
            address="123 Main St"
        )

        self.order = Order.objects.create(
            user=self.user, order_date=timezone.now(), total_amount=100.00
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='password456',
            email='otheruser@example.com',
            address="456 Another St"
        )

    def test_order_detail_view_authenticated(self):
        
        self.client.force_login(self.user)

        response = self.client.get(reverse('Orders:order_detail', args=[self.order.id]))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, str(self.order.total_amount))

    def test_order_detail_view_other_user(self):
        
        self.client.force_login(self.other_user)

        response = self.client.get(reverse('Orders:order_detail', args=[self.order.id]))

        self.assertEqual(response.status_code, 404)
