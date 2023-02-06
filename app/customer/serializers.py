"""
Serializers for customer APIs
"""
from rest_framework import serializers

from core.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for customers."""

    class Meta:
        model = Customer
        fields = ['id', 'name']
        read_only_fields = ['id']

class CustomerDetailSerializer(CustomerSerializer):
    """Serializer for customer detail view"""
    class Meta:
        model = Customer
        fields = ['id', 'name', 'age']
        read_only_fields = ['id']


