from rest_framework import serializers
from .models import HealthEvent, ReminderNotification

class HealthEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthEvent
        fields = '__all__'

class ReminderNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReminderNotification
        fields = '__all__'
