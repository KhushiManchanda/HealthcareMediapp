from django.db import models

class Questionnaire(models.Model):
    """Dynamic forms assigned to patients before visits."""
    clinic = models.ForeignKey('users.Clinic', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text="e.g., Initial Intake Form, Covid Screening")
    description = models.TextField(blank=True)

class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=20, choices=[('text', 'Text'), ('single_choice', 'Single Choice'), ('scale', '1-10 Scale')])
    options = models.JSONField(default=list, blank=True)

class PatientSubmission(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    patient = models.ForeignKey('users.ClinicUser', on_delete=models.CASCADE)
    answers = models.JSONField(help_text="Dict of question ID to answer payload")
    submitted_at = models.DateTimeField(auto_now_add=True)
