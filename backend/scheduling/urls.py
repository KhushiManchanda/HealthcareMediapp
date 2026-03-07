from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthEventViewSet, ReminderNotificationViewSet, BookAppointmentView, UnifiedCalendarView

router = DefaultRouter()
router.register(r'events', HealthEventViewSet, basename='events')
router.register(r'reminders', ReminderNotificationViewSet, basename='reminders')

urlpatterns = [
    path('unified/', UnifiedCalendarView.as_view(), name='calendar-unified'),
    path('book/', BookAppointmentView.as_view(), name='book-appointment'),
    path('', include(router.urls)),
]
