"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
import datetime



def workout_image_file_path(instance, filename):
    """Generate file path for new workout image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'workout', filename)



class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Workout(models.Model):
    """Workout object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=workout_image_file_path)

class Section(models.Model):
    """Section object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=255)
    rest_time = models.CharField(max_length=50)
    reps = models.CharField(max_length=20)
    workouts = models.ManyToManyField(Workout, through='Section_Workout', related_name='section_workout_mtm', blank=True)

    def __str__(self):
        return self.description


class Training(models.Model):
    """Training object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=255)
    date = models.DateField(null=True)
    sections = models.ManyToManyField(Section, through='Training_Section', related_name='training_section_mtm', blank=True)

    def __str__(self):
        return self.description



class Training_Section(models.Model):
    training = models.ForeignKey(Training, on_delete=models.PROTECT, related_name='training_fk')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='training_section_fk')

    def __str__(self):
        return self.section.description



class Section_Workout(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.PROTECT, related_name='workout_fk')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section_workout_fk')
    reps_workout = models.CharField(max_length=20)

    def __str__(self):
        return self.section.description +' Workout: '+ self.workout.name




