from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import HealthEvent
from users.models import ClinicUser

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
            doctor_profile = ClinicUser.objects.get(id=doctor_id, role='doctor')
        except ClinicUser.DoesNotExist:
            return Response({"error": "Invalid doctor ID provided"}, status=status.HTTP_404_NOT_FOUND)

        appointment = HealthEvent.objects.create(
            patient=patient_profile,
            doctor=doctor_profile,
            event_type='appointment',
            title=title,
            start_datetime=start_datetime,
            status='scheduled'
        )

        # The signal in scheduling/signals.py will automatically run post_save to create a Chat Room
        return Response({
            "success": True, 
            "message": "Appointment booked and Chat room bridged successfully.",
            "appointment_id": appointment.id
        }, status=status.HTTP_201_CREATED)
