from django.db import models
import uuid

class MedicalDocument(models.Model):
    STATUS_CHOICES = (('uploaded', 'Uploaded'), ('processing', 'Processing OCR/NLP'), ('completed', 'Completed'), ('flagged', 'Needs Doctor Review'))
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('users.ClinicUser', on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    document_type = models.CharField(max_length=50, choices=[('lab_report', 'Lab Report'), ('prescription', 'Prescription'), ('scan', 'Scan')])
    file = models.FileField(upload_to='medical_records/')
    
    raw_ocr_text = models.TextField(blank=True)
    ai_summary = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ExtractedMetric(models.Model):
    """Derived directly from MedicalDocument via LLM."""
    document = models.ForeignKey(MedicalDocument, on_delete=models.CASCADE, related_name='metrics')
    metric_name = models.CharField(max_length=100, help_text="e.g., Fasting Blood Sugar")
    value = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, blank=True)
    reference_range = models.CharField(max_length=100, blank=True)
    is_abnormal = models.BooleanField(default=False)
    measured_date = models.DateField(null=True, blank=True)
