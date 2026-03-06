from django.contrib import admin
from .models import HealthEvent, ReminderNotification

admin.site.register(HealthEvent)
admin.site.register(ReminderNotification)
