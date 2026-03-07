from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
from .models import HealthEvent, ReminderNotification
from .serializers import HealthEventSerializer, ReminderNotificationSerializer
from .services import SchedulingService, SchedulingAggregationService

class BookAppointmentView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # We assume request.user maps to a single patient ClinicUser for simplicity,
        # or it is passed directly in payload. In our architecture, the user has 
        # a ClinicUser representation. 
        patient_profile = request.user.clinic_profiles.filter(role='patient').first()
        
        if not patient_profile:
            return Response({"error": "You must be registered as a patient to book an appointment."}, status=status.HTTP_400_BAD_REQUEST)

        doctor_id = request.data.get('doctor_id')
        start_datetime = request.data.get('start_datetime')
        title = request.data.get('title', 'Initial Consultation')

        if not all([doctor_id, start_datetime]):
            return Response({"error": "doctor_id and start_datetime are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            appointment = SchedulingService.book_appointment(
                patient_profile=patient_profile,
                doctor_id=doctor_id,
                start_datetime=start_datetime,
                title=title
            )
            return Response({
                "success": True, 
                "message": "Appointment booked and Chat room bridged successfully.",
                "appointment_id": appointment.id
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class HealthEventViewSet(viewsets.ModelViewSet):
    queryset = HealthEvent.objects.all()
    serializer_class = HealthEventSerializer
    permission_classes = [IsAuthenticated]

class ReminderNotificationViewSet(viewsets.ModelViewSet):
    queryset = ReminderNotification.objects.all()
    serializer_class = ReminderNotificationSerializer
    permission_classes = [IsAuthenticated]

class UnifiedCalendarView(views.APIView):
    """
    Unified calendar endpoint that aggregates patient/doctor events from multiple sources
    (Analogous to Unio's apps.calendar.views.UnifiedCalendarView).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.clinic_profiles.first()
        if not user:
            return Response({"error": "No associated clinical profile mapped."}, status=403)

        start_str = request.query_params.get('start_date')
        end_str = request.query_params.get('end_date')
        types_str = request.query_params.get('types')

        start_date = None
        end_date = None
        
        if start_str:
            try:
                start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        if end_str:
            try:
                end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        event_types = [t.strip() for t in types_str.split(',')] if types_str else None

        service = SchedulingAggregationService(user=user)
        events = service.get_unified_events(
            start_date=start_date,
            end_date=end_date,
            event_types=event_types
        )

        return Response({
            'count': len(events),
            'results': events
        })

