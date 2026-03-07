from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MedicalDocument, ExtractedMetric
from .serializers import MedicalDocumentSerializer, ExtractedMetricSerializer

class MedicalDocumentViewSet(viewsets.ModelViewSet):
    queryset = MedicalDocument.objects.all()
    serializer_class = MedicalDocumentSerializer
    permission_classes = [IsAuthenticated]

    # Note: AI OCR scanning logic via Celery will be triggered within perform_create()

class ExtractedMetricViewSet(viewsets.ModelViewSet):
    queryset = ExtractedMetric.objects.all()
    serializer_class = ExtractedMetricSerializer
    permission_classes = [IsAuthenticated]
