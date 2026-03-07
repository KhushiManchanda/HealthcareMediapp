from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalDocumentViewSet, ExtractedMetricViewSet

router = DefaultRouter()
router.register(r'documents', MedicalDocumentViewSet, basename='medical-documents')
router.register(r'metrics', ExtractedMetricViewSet, basename='extracted-metrics')

urlpatterns = [
    path('', include(router.urls)),
]
