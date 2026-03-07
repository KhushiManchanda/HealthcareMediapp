from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClinicViewSet, UserViewSet, ClinicUserViewSet, FamilyRelationshipViewSet

router = DefaultRouter()
router.register(r'clinics', ClinicViewSet, basename='clinics')
router.register(r'base-users', UserViewSet, basename='base-users')
router.register(r'clinic-users', ClinicUserViewSet, basename='clinic-users')
router.register(r'family-relationships', FamilyRelationshipViewSet, basename='family-relationships')

urlpatterns = [
    path('', include(router.urls)),
]
