"""
Tests for customer APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Customer

from customer.serializers import (
    CustomerSerializer,
    CustomerDetailSerializer,
)


CUSTOMERS_URL = reverse('customer:customer-list')

def detail_url(customer_id):
    """Create and return a customer detail url"""
    return reverse('customer:customer-detail', args=[customer_id])


def create_customer(user, **params):
    """Create and return a sample customer."""
    defaults = {
        'name': 'Son Bubu',
        'age': 22,
    }
    defaults.update(params)

    customer = Customer.objects.create(user=user, **defaults)
    return customer


class PublicCustomerAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(CUSTOMERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCustomerApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_customers(self):
        """Test retrieving a list of customers."""
        create_customer(user=self.user)
        create_customer(user=self.user)

        res = self.client.get(CUSTOMERS_URL)

        customers = Customer.objects.all().order_by('-id')
        serializer = CustomerSerializer(customers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_customer_list_limited_to_user(self):
        """Test list of customers is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_customer(user=other_user)
        create_customer(user=self.user)

        res = self.client.get(CUSTOMERS_URL)

        customers = Customer.objects.filter(user=self.user)
        serializer = CustomerSerializer(customers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_customer_detail(self):
        """Test get customer detail"""
        customer = create_customer(user=self.user)

        url = detail_url(customer.id)
        res = self.client.get(url)

        serializer = CustomerDetailSerializer(customer)
        self.assertEqual(res.data, serializer.data)

    def test_create_customer(self):
        """test creating customer"""
        payload = {
            'name': 'Bubu',
            'age' : 26,
        }
        res = self.client.post(CUSTOMERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        customer = Customer.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(customer,k), v)
        self.assertEqual(customer.user, self.user)
