from django.db import models

class DoctorProfile(models.Model):
    clinic_user = models.OneToOneField('users.ClinicUser', on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    medical_registration_no = models.CharField(max_length=100, unique=True)
    specialty = models.CharField(max_length=255)
    qualifications = models.TextField(help_text="e.g., MBBS, MD (Cardiology)")
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bio = models.TextField(blank=True)
    availability_schedule = models.JSONField(default=dict, help_text="Weekly availability matrix")

class PatientProfile(models.Model):
    clinic_user = models.OneToOneField('users.ClinicUser', on_delete=models.CASCADE, limit_choices_to={'role': 'patient'})
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    blood_group = models.CharField(max_length=5, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Critical Health Data
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True, help_text="e.g., Diabetes, Hypertension")
    current_medications = models.TextField(blank=True)
