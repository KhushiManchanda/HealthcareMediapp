from rest_framework import serializers
from .models import Clinic, User, ClinicUser, FamilyRelationship

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

class ClinicUserSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)

    class Meta:
        model = ClinicUser
        fields = ['id', 'user', 'user_details', 'clinic', 'clinic_name', 'role', 'is_active']

class FamilyRelationshipSerializer(serializers.ModelSerializer):
    guardian_details = ClinicUserSerializer(source='guardian', read_only=True)
    patient_details = ClinicUserSerializer(source='patient', read_only=True)

    class Meta:
        model = FamilyRelationship
        fields = '__all__'
