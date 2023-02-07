"""
Views for the section APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Section
from section import serializers


class SectionViewSet(viewsets.ModelViewSet):
    """View for manage section APIs."""
    serializer_class = serializers.SectionDetailSerializer
    queryset = Section.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve sections for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return serializer class for request"""
        if self.action == 'list':
            return serializers.SectionSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new section"""
        serializer.save(user=self.request.user)