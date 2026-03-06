from django.db import models
import uuid

class TriageSession(models.Model):
    SEVERITY_CHOICES = (('low', 'Routine Care'), ('medium', 'Monitor Closely'), ('high', 'Urgent / Doctor Needed'))
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('users.ClinicUser', on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    
    primary_symptom = models.CharField(max_length=255, blank=True)
    severity_assessment = models.CharField(max_length=20, choices=SEVERITY_CHOICES, blank=True)
    
    started_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class TriageMessage(models.Model):
    session = models.ForeignKey(TriageSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[('patient', 'Patient'), ('ai', 'AI Assistant')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class ClinicalSummary(models.Model):
    """The final payload sent to the doctor."""
    session = models.OneToOneField(TriageSession, on_delete=models.CASCADE)
    doctor_assigned = models.ForeignKey('users.ClinicUser', null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'role': 'doctor'})
    chief_complaint = models.TextField()
    ai_analysis = models.TextField(help_text="Differential diagnosis / AI thought process")
    recommended_action = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
