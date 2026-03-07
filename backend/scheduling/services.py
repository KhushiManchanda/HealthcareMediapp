from datetime import datetime, timedelta
from django.utils import timezone
from .models import HealthEvent
from users.models import ClinicUser

class SchedulingService:
    """
    Handles complex business logic for appointments and health events, 
    keeping the views.py clean as per Unio architectures.
    """

    @staticmethod
    def book_appointment(patient_profile, doctor_id, start_datetime, title="Initial Consultation"):
        """
        Creates an appointment completely validating doctor availability and types.
        """
        try:
            doctor_profile = ClinicUser.objects.get(id=doctor_id, role='doctor')
        except ClinicUser.DoesNotExist:
            raise ValueError("Invalid doctor ID provided")

        appointment = HealthEvent.objects.create(
            patient=patient_profile,
            doctor=doctor_profile,
            event_type='appointment',
            title=title,
            start_datetime=start_datetime,
            status='scheduled'
        )
        
        return appointment

class SchedulingAggregationService:
    """Service to aggregate and format all health events (Calendar view)."""

    def __init__(self, user):
        self.user = user

    def get_unified_events(self, start_date=None, end_date=None, event_types=None):
        """
        Get unified calendar events specifically scoped to this user's role 
        (e.g., patient viewing their medicines/appointments, doctor viewing their bookings).
        """
        if not start_date:
            start_date = timezone.now().date().replace(day=1)
        if not end_date:
            next_month = start_date.replace(day=28) + timedelta(days=4)
            end_date = next_month.replace(day=1) + timedelta(days=30)

        fetch_all = event_types is None
        event_types = event_types or []
        events = []

        # Assuming user is a ClinicUser context
        queryset = HealthEvent.objects.filter(
            start_datetime__date__gte=start_date,
            start_datetime__date__lte=end_date
        )

        if self.user.role == 'patient':
            queryset = queryset.filter(patient=self.user)
        elif self.user.role == 'doctor':
            queryset = queryset.filter(doctor=self.user)
        else:
            queryset = queryset.none()

        if not fetch_all:
            queryset = queryset.filter(event_type__in=event_types)

        for e in queryset:
            color_map = {
                'appointment': '#3357FF',  # Blue
                'medicine': '#FF5733',     # Red/Orange
                'measurement': '#33FF57',  # Green
            }

            end_dt = e.end_datetime if e.end_datetime else e.start_datetime + timedelta(minutes=30)

            events.append({
                'id': f'{e.event_type}-{e.id}',
                'event_type': e.event_type,
                'source_id': e.id,
                'title': e.title,
                'description': e.description,
                'start_datetime': e.start_datetime.isoformat(),
                'end_datetime': end_dt.isoformat(),
                'is_recurring': e.is_recurring,
                'recurrence_rule': e.recurrence_rule,
                'status': e.status,
                'editable': e.status == 'scheduled',
                'color': color_map.get(e.event_type, '#808080'),
                'doctor_name': f"Dr. {e.doctor.user.get_full_name()}" if e.doctor and e.doctor.user else None,
                'patient_name': e.patient.user.get_full_name() if e.patient and e.patient.user else None,
            })

        # Sort chronologically
        events.sort(key=lambda x: x['start_datetime'])
        return events
