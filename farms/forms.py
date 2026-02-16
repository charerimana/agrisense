from django import forms
from .models import Farm, NotificationPreference

class FarmSensorForm(forms.ModelForm):
    # Add Sensor fields manually to the Farm form
    min_temp = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_temp = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Farm
        fields = ['name', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing, pre-fill the sensor fields
        if self.instance and hasattr(self.instance, 'sensor'):
            self.fields['min_temp'].initial = self.instance.sensor.min_temp
            self.fields['max_temp'].initial = self.instance.sensor.max_temp

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        location = cleaned_data.get('location')
        owner = self.instance.owner # The owner assigned in the view

        # Check for duplicates, excluding the current instance (important for Updates)
        exists = Farm.objects.filter(
            owner=owner, 
            name__iexact=name, 
            location=location
        ).exclude(pk=self.instance.pk).exists()

        if exists:
            # This error will show up next to the 'name' field in html modal
            self.add_error('name', f"You already have a farm named '{name}' in {location}.")
        
        return cleaned_data


class NotificationPreferenceForm(forms.ModelForm):
    class Meta:
        model = NotificationPreference
        fields = ['alerts_enabled', 'email_enabled', 'sms_enabled', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        sms_enabled = cleaned_data.get('sms_enabled')
        phone_number = cleaned_data.get('phone_number')

        if sms_enabled and not phone_number:
            self.add_error('phone_number', "This field is required when SMS is enabled.")

        if phone_number:
            import re
            if not re.match(r'^\+?2507[2389]\d{7}$', phone_number):
                self.add_error('phone_number', "Phone number must be in format: '+2507....'.")

        return cleaned_data

