from django import forms
from .models import DailyAffirmation, EmergencyContact

class DailyAffirmationForm(forms.ModelForm):
    class Meta:
        model = DailyAffirmation
        fields = ['text']

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'phone_number']