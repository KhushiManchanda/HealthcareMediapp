from rest_framework import serializers
from .models import MedicalDocument, ExtractedMetric

class ExtractedMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedMetric
        fields = '__all__'

class MedicalDocumentSerializer(serializers.ModelSerializer):
    metrics = ExtractedMetricSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalDocument
        fields = '__all__'
