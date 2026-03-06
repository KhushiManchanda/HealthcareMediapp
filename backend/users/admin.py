from django.contrib import admin
from .models import Clinic, User, ClinicUser, FamilyRelationship

admin.site.register(Clinic)
admin.site.register(User)
admin.site.register(ClinicUser)
admin.site.register(FamilyRelationship)
