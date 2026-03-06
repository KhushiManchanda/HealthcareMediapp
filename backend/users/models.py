from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Clinic(models.Model):
    """Equivalent to 'Organization' in LMS. Represents a hospital or clinic instance."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    """Base custom user model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

class ClinicUser(models.Model):
    """Equivalent to 'OrganizationUser'."""
    ROLE_CHOICES = (
        ('admin', 'Clinic Admin'),
        ('doctor', 'Doctor / Specialist'),
        ('patient', 'Patient / Family Member'),
        ('guardian', 'Family Head / Guardian'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinic_profiles')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('user', 'clinic')

class FamilyRelationship(models.Model):
    """Equivalent to 'ParentStudentRelationship'."""
    RELATIONSHIP_CHOICES = (('mother', 'Mother'), ('father', 'Father'), ('child', 'Child'), ('spouse', 'Spouse'), ('other', 'Other'))
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guardian = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='dependents', limit_choices_to={'role': 'guardian'})
    patient = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='guardians', limit_choices_to={'role': 'patient'})
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    is_primary_emergency_contact = models.BooleanField(default=False)
