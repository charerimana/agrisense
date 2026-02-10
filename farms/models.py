from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Farm(models.Model):
    RWANDA_DISTRICT_CHOICES = [
      ('Kigali City', (
          ('Nyarugenge', 'Nyarugenge'),
          ('Gasabo', 'Gasabo'),
          ('Kicukiro', 'Kicukiro'),
      )),
      ('Eastern Province', (
          ('Nyagatare', 'Nyagatare'),
          ('Gatsibo', 'Gatsibo'),
          ('Kayonza', 'Kayonza'),
          ('Rwamagana', 'Rwamagana'),
          ('Bugesera', 'Bugesera'),
          ('Ngoma', 'Ngoma'),
          ('Kirehe', 'Kirehe'),
      )),
      ('Northern Province', (
          ('Musanze', 'Musanze'),
          ('Burera', 'Burera'),
          ('Gicumbi', 'Gicumbi'),
          ('Rulindo', 'Rulindo'),
          ('Gakenke', 'Gakenke'),
      )),
      ('Southern Province', (
          ('Huye', 'Huye'),
          ('Nyamagabe', 'Nyamagabe'),
          ('Gisagara', 'Gisagara'),
          ('Nyanza', 'Nyanza'),
          ('Nyaruguru', 'Nyaruguru'),
          ('Muhanga', 'Muhanga'),
          ('Kamonyi', 'Kamonyi'),
          ('Ruhango', 'Ruhango'),
      )),
      ('Western Province', (
          ('Rubavu', 'Rubavu'),
          ('Rusizi', 'Rusizi'),
          ('Karongi', 'Karongi'),
          ('Nyabihu', 'Nyabihu'),
          ('Rutsiro', 'Rutsiro'),
          ('Ngororero', 'Ngororero'),
          ('Nyamasheke', 'Nyamasheke'),
      )),
    ]
      
    name = models.CharField(max_length=100)
    location = models.CharField(
        max_length=50, 
        choices=RWANDA_DISTRICT_CHOICES,
        default='Gasabo'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="farms"
    )

    def __str__(self):
        return self.name


class Sensor(models.Model):
    SENSOR_TYPE_CHOICES = [
        ("TEMP", "Temperature"),
    ]

    farm = models.OneToOneField(
        Farm,
        on_delete=models.CASCADE,
        related_name="sensor"
    )
    sensor_type = models.CharField(
        max_length=10,
        choices=SENSOR_TYPE_CHOICES,
        default="TEMP"
    )
    min_temp = models.FloatField()
    max_temp = models.FloatField()

    def __str__(self):
        return f"Sensor for {self.farm.name}"


class SensorReading(models.Model):
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name="readings"
    )
    temperature = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.temperature}°C at {self.recorded_at}"
    

class NotificationPreference(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="notification_preference"
    )
    alerts_enabled = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        default=""
    )

    def __str__(self):
        return f"Preferences for {self.user}"


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ("EMAIL", "Email"),
        ("SMS", "SMS"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    reading = models.ForeignKey(
        SensorReading,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    message = models.TextField()
    notification_type = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPE_CHOICES
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} to {self.user}"
