from django.db import models
import uuid

class HealthEvent(models.Model):
    EVENT_TYPES = (
        ('appointment', 'Doctor Appointment'),
        ('medicine', 'Medicine Reminder'),
        ('measurement', 'Vitals Tracker (e.g., BP check)'),
    )
    STATUS_CHOICES = (('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey('users.ClinicUser', on_delete=models.CASCADE, related_name='health_events')
    doctor = models.ForeignKey('users.ClinicUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    
    # For Medicine Trackers
    is_recurring = models.BooleanField(default=False)
    recurrence_rule = models.CharField(max_length=255, blank=True, help_text="RRULE string for daily/weekly pills")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

class ReminderNotification(models.Model):
    event = models.ForeignKey(HealthEvent, on_delete=models.CASCADE, related_name='reminders')
    remind_before_minutes = models.IntegerField(default=15)
    sent = models.BooleanField(default=False)
