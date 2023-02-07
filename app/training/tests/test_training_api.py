"""
Tests for training APIs.
"""
from django.utils import timezone
import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Training

from training.serializers import (
    TrainingSerializer,
    TrainingDetailSerializer,
)


TRAININGS_URL = reverse('training:training-list')


def detail_url(training_id):
    """Create and return a training detail url"""
    return reverse('training:training-detail', args=[training_id])


def create_training(user, **params):
    """Create and return a sample training."""
    date = datetime.date(1997, 10, 19)
    defaults = {
        'description': 'TreinoFuncional',
        'date' : date,
    }
    defaults.update(params)

    training = Training.objects.create(user=user, **defaults)
    return training

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

class PublicTrainingAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(TRAININGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTrainingApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_trainings(self):
        """Test retrieving a list of trainings."""
        create_training(user=self.user)
        create_training(user=self.user)

        res = self.client.get(TRAININGS_URL)

        trainings = Training.objects.all().order_by('-id')
        serializer = TrainingSerializer(trainings, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_training_list_limited_to_user(self):
        """Test list of trainings is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_training(user=other_user)
        create_training(user=self.user)

        res = self.client.get(TRAININGS_URL)

        trainings = Training.objects.filter(user=self.user)
        serializer = TrainingSerializer(trainings, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_training_detail(self):
        """Test get training detail"""
        training = create_training(user=self.user)

        url = detail_url(training.id)
        res = self.client.get(url)

        serializer = TrainingDetailSerializer(training)
        self.assertEqual(res.data, serializer.data)

    def test_create_training(self):
        """test creating training"""
        date = datetime.date(1997, 10, 19)
        payload = {
            'description':'TreinoFuncional',
            'date':date,
        }
        res = self.client.post(TRAININGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        training = Training.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(training,k), v)
        self.assertEqual(training.user, self.user)
