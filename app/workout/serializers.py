"""
Serializers for workout APIs
"""
from rest_framework import serializers


from core.models import Workout


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for workouts."""

    class Meta:
        model = Workout
        fields = ['id', 'name']
        read_only_fields = ['id']

class WorkoutDetailSerializer(WorkoutSerializer):
    """Serializer for workout detail view"""

    class Meta:
        model = Workout
        fields = ['id', 'name','image']
        read_only_fields = ['id']

class WorkoutImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to workouts."""

    class Meta:
        model = Workout
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}

