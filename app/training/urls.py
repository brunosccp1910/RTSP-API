"""Urls mappings for the recipe app"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from training import views

router = DefaultRouter()
router.register('trainings',views.TrainingViewSet)

app_name = 'training'

urlpatterns = [
    path('', include(router.urls))
]