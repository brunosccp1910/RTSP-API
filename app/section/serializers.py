"""
Serializers for section APIs
"""
from rest_framework import serializers


from core.models import Section, Workout


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for workouts."""

    class Meta:
        model = Workout
        fields = ['id', 'name', 'image']
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

class SectionDetailSerializer(SectionSerializer):
    """Serializer for section detail view"""

    class Meta:
        model = Section
        fields = ['id', 'description','rest_time','reps','workouts']
        read_only_fields = ['id']


