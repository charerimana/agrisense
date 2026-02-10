from django.contrib import admin
from .models import (
    Farm,
    Sensor,
    SensorReading,
    Notification,
    NotificationPreference
)

# Register your models here.
admin.site.register(Farm)
admin.site.register(Sensor)
admin.site.register(SensorReading)
admin.site.register(Notification)
admin.site.register(NotificationPreference)
