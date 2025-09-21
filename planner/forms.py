from django import forms
from .models import Event
from django.forms import DateTimeInput

class SettingsForm(forms.Form):
    THEME_CHOICES = [('light','Светлая'), ('dark','Тёмная')]
    LANG_CHOICES = [('ru','Русский'), ('en','English')]
    theme = forms.ChoiceField(choices=THEME_CHOICES, required=False)
    language = forms.ChoiceField(choices=LANG_CHOICES, required=False)
    notifications = forms.BooleanField(required=False, label='Уведомления включены')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date_time', 'location', 'image']
        widgets = {
            'date_time': DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows':4}),
        }
class SettingsForm(forms.Form):
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Тёмная'),
    ]
    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'English'),
    ]
    
    theme = forms.ChoiceField(choices=THEME_CHOICES, widget=forms.RadioSelect)
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, widget=forms.RadioSelect)
    notifications = forms.BooleanField(required=False, label="Включить уведомления")