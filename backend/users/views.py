from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Clinic, User, ClinicUser, FamilyRelationship
from .serializers import ClinicSerializer, UserSerializer, ClinicUserSerializer, FamilyRelationshipSerializer

class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ClinicUserViewSet(viewsets.ModelViewSet):
    queryset = ClinicUser.objects.all()
    serializer_class = ClinicUserSerializer
    permission_classes = [IsAuthenticated]

class FamilyRelationshipViewSet(viewsets.ModelViewSet):
    queryset = FamilyRelationship.objects.all()
    serializer_class = FamilyRelationshipSerializer
    permission_classes = [IsAuthenticated]

