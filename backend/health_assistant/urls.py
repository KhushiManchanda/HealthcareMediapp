from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TriageSessionViewSet, ClinicalSummaryViewSet

router = DefaultRouter()
router.register(r'sessions', TriageSessionViewSet, basename='triage-sessions')
router.register(r'summaries', ClinicalSummaryViewSet, basename='clinical-summaries')

urlpatterns = [
    path('', include(router.urls)),
]
