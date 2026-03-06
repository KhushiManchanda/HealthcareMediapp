from django.contrib import admin
from .models import MedicalDocument, ExtractedMetric

admin.site.register(MedicalDocument)
admin.site.register(ExtractedMetric)
