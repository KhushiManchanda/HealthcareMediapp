from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DoctorProfile, PatientProfile
from .serializers import DoctorProfileSerializer, PatientProfileSerializer

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]
