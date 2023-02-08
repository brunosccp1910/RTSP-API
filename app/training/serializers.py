"""
Serializers for training APIs
"""
from rest_framework import serializers
from django.utils import timezone
import datetime

from core.models import Training, Section, Workout, Section_Workout

class Section_Workout_Serializer(serializers.ModelSerializer):
    """Serializer for sections_workouts."""

    class Meta:
        model = Section_Workout
        fields = ['id', 'reps_workout']
        read_only_fields = ['id']

class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for workouts."""

    section_workout = Section_Workout_Serializer(many=True, required=False)

    class Meta:
        model = Workout
        fields = ['id', 'name', 'image','section_workout']
        read_only_fields = ['id']

class SectionSerializer(serializers.ModelSerializer):
    """Serializer for sections."""

    workouts = WorkoutSerializer(many=True, required=False)

    class Meta:
        model = Section
        fields = ['id', 'description','workouts']
        read_only_fields = ['id']

    def _get_or_create_workouts(self, workouts, section):
        """Handle getting or creating workouts as needed."""
        auth_user = self.context['request'].user
        for workout in workouts:
            workout_obj, created = Workout.objects.get_or_create(
                user=auth_user,
                **workout,
            )
            section.workouts.add(workout_obj)

    def create(self, validated_data):
        """Create a section."""
        workouts = validated_data.pop('workouts', [])
        section = Section.objects.create(**validated_data)
        self._get_or_create_workouts(workouts, section)

        return section

    def update(self, instance, validated_data):
        """Update section."""
        workouts = validated_data.pop('workouts', None)
        if workouts is not None:
            instance.workouts.clear()
            self._get_or_create_workouts(workouts, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TrainingSerializer(serializers.ModelSerializer):
    """Serializer for trainings."""
    sections = SectionSerializer(many=True, required=False)
    class Meta:
        model = Training
        fields = ['id', 'description','sections']
        read_only_fields = ['id']

    def _get_or_create_sections(self, sections, training):
        """Handle getting or creating sections as needed."""
        auth_user = self.context['request'].user
        for section in sections:
            section_obj, created = Section.objects.get_or_create(
                user=auth_user,
                **section,
            )
            training.sections.add(section_obj)

    def create(self, validated_data):
        """Create a section."""
        sections = validated_data.pop('sections', [])
        training = Training.objects.create(**validated_data)
        self._get_or_create_sections(sections, training)

        return training

    def update(self, instance, validated_data):
        """Update section."""
        sections = validated_data.pop('sections', None)
        if sections is not None:
            instance.sections.clear()
            self._get_or_create_sections(sections, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TrainingDetailSerializer(TrainingSerializer):
    """Serializer for training detail view"""
    date = serializers.DateField()

    class Meta:
        model = Training
        fields = ['id', 'description','date','sections']
        read_only_fields = ['id']


