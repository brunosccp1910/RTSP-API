
"""
Tests for section APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Section

from section.serializers import (
    SectionSerializer,
    SectionDetailSerializer,
)


SECTIONS_URL = reverse('section:section-list')


def detail_url(section_id):
    """Create and return a section detail url"""
    return reverse('section:section-detail', args=[section_id])


def create_section(user, **params):
    """Create and return a sample section."""
    defaults = {
        'description': 'Bloco1',
        'rest_time' : '3',
        'reps': '1',
    }
    defaults.update(params)

    section = Section.objects.create(user=user, **defaults)
    return section

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicSectionAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(SECTIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSectionApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)


    def test_retrieve_sections(self):
        """Test retrieving a list of sections."""
        create_section(user=self.user)
        create_section(user=self.user)

        res = self.client.get(SECTIONS_URL)

        sections = Section.objects.all().order_by('-id')
        serializer = SectionSerializer(sections, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_create_section(self):
        payload = {
            'description':'Bloco1',
            'rest_time':'3',
            'reps':'1'
        }

        res = self.client.post(SECTIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        section = Section.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(section,k), v)
        self.assertEqual(section.user, self.user)


