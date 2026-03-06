from django.contrib import admin
from .models import Questionnaire, Question, PatientSubmission

admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(PatientSubmission)
