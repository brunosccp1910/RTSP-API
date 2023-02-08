"""
Views for the workout APIs
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Workout
from workout import serializers


class WorkoutViewSet(viewsets.ModelViewSet):
    """View for manage workout APIs."""
    serializer_class = serializers.WorkoutDetailSerializer
    queryset = Workout.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve workouts for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return serializer class for request"""
        if self.action == 'list':
            return serializers.WorkoutSerializer
        elif self.action == 'upload_image':
            return serializers.WorkoutImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new workout"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to workout."""
        workout = self.get_object()
        serializer = self.get_serializer(workout, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)