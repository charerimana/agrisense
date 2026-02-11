from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Farm, Sensor, SensorReading, Notification, NotificationPreference

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Farm.objects.all(),
                fields=['owner', 'name', 'location'],
                message="This farm already exists in your account."
            )
        ]


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"


class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = "__all__"


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = "__all__"

    def validate(self, data):
        sms_enabled = data.get('sms_enabled', getattr(self.instance, 'sms_enabled', False))
        phone_number = data.get('phone_number', getattr(self.instance, 'phone_number', ''))

        if sms_enabled and not phone_number:
            raise serializers.ValidationError({
                "phone_number": "This field is required when SMS is enabled."
            })

        if phone_number:
            import re
            # Matches +25078..., 078..., etc.
            if not re.match(r'^\+?2507[2389]\d{7}$', phone_number):
                raise serializers.ValidationError({
                    "phone_number": "Phone number must be entered in the format: '+2507....'."
                })

        return data

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
