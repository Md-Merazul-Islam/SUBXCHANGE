from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import Plan, Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.plan = Plan.objects.create(
            name='Test Plan',
            price=Decimal('19.99'),
            duration_days=30
        )

    def test_subscription_creation(self):
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan
        )
        self.assertEqual(subscription.status, 'active')
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.plan, self.plan)


class SubscriptionAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.plan = Plan.objects.create(
            name='Test Plan',
            price=Decimal('19.99'),
            duration_days=30
        )

    def test_subscribe_to_plan(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('subscribe')
        data = {'plan_id': self.plan.id}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertEqual(Subscription.objects.count(), 1)

    def test_list_user_subscriptions(self):
        self.client.force_authenticate(user=self.user)

        # Create a subscription
        Subscription.objects.create(user=self.user, plan=self.plan)

        url = reverse('user-subscriptions')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_cancel_subscription(self):
        self.client.force_authenticate(user=self.user)

        # Create a subscription
        subscription = Subscription.objects.create(
            user=self.user, plan=self.plan)

        url = reverse('cancel-subscription')
        data = {'subscription_id': subscription.id}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

        subscription.refresh_from_db()
        self.assertEqual(subscription.status, 'cancelled')


