from django import forms
from .models import Farm

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
