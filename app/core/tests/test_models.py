"""
Tests for models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

from core import models

def create_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_training(self):
        """Test creating a training is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        datetest = datetime.date(1997, 10, 19)
        training = models.Training.objects.create(
            user=user,
            description='TreinoFuncional',
            date = datetest,
        )

        self.assertEqual(str(training), training.description)

    def test_create_section(self):
        """Test creating a section is sucessful"""

        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        section = models.Section.objects.create(
            user=user,
            description = 'Bloco1',
            rest_time='1',
            reps='3',

        )

        self.assertEqual(str(section), section.description)
"""
    def test_create_workout(self):
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        workout = models.Workout.objects.create(
            user=user,
            description = 'Burp',
            reps = '15',

        )
"""