"""Urls mappings for the recipe app"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from section import views

router = DefaultRouter()
router.register('sections',views.SectionViewSet)

app_name = 'section'

urlpatterns = [
    path('', include(router.urls))
]