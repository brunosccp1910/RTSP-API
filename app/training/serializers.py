"""
Serializers for training APIs
"""
from rest_framework import serializers
from django.utils import timezone
import datetime

from core.models import Training


class TrainingSerializer(serializers.ModelSerializer):
    """Serializer for trainings."""

    class Meta:
        model = Training
        fields = ['id', 'description']
        read_only_fields = ['id']

class TrainingDetailSerializer(TrainingSerializer):
    """Serializer for training detail view"""
    date = serializers.DateField()

    class Meta:
        model = Training
        fields = ['id', 'description','date']
        read_only_fields = ['id']


