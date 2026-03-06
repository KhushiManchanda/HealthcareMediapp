from django.contrib import admin
from .models import TriageSession, TriageMessage, ClinicalSummary

admin.site.register(TriageSession)
admin.site.register(TriageMessage)
admin.site.register(ClinicalSummary)
