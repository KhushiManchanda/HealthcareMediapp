from rest_framework import serializers
from .models import TriageSession, TriageMessage, ClinicalSummary

class TriageMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriageMessage
        fields = '__all__'

class ClinicalSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalSummary
        fields = '__all__'

class TriageSessionSerializer(serializers.ModelSerializer):
    messages = TriageMessageSerializer(many=True, read_only=True)
    summary = ClinicalSummarySerializer(read_only=True, source='clinicalsummary')

    class Meta:
        model = TriageSession
        fields = '__all__'
