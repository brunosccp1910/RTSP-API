"""
Views for the training APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Training
from training import serializers


class TrainingViewSet(viewsets.ModelViewSet):
    """View for manage training APIs."""
    serializer_class = serializers.TrainingDetailSerializer
    queryset = Training.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve trainings for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return serializer class for request"""
        if self.action == 'list':
            return serializers.TrainingSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new training"""
        serializer.save(user=self.request.user)