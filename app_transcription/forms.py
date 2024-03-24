from django import forms
from django.forms import TextInput, FileInput

from app_transcription.models import Recording, APIClient


class RecordingCreateForm(forms.ModelForm):
    class Meta:
        model = Recording
        fields = ['name', 'audio_file']

        widgets = {
            'name': TextInput(attrs={'placeholder': 'Please enter name for this recording', 'class': 'form-control'}),
            'audio_file': FileInput(attrs={'class': 'form-control', 'accept': 'audio/*'}),
        }


class APIClientCreateForm(forms.ModelForm):
    class Meta:
        model = APIClient
        fields = ['client_name', 'api_key']
        labels = {'api_key': 'API key (auto-generated)'}

        widgets = {
            'client_name': TextInput(
                attrs={'placeholder': 'Please enter name for this client', 'class': 'form-control'}),
            'api_key': TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
