"""
Serializers for section APIs
"""
from rest_framework import serializers


from core.models import Section


class SectionSerializer(serializers.ModelSerializer):
    """Serializer for sections."""

    class Meta:
        model = Section
        fields = ['id', 'description']
        read_only_fields = ['id']

class SectionDetailSerializer(SectionSerializer):
    """Serializer for section detail view"""
    date = serializers.DateField()

    class Meta:
        model = Section
        fields = ['id', 'description','rest_time','reps']
        read_only_fields = ['id']


