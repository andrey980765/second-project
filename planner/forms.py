from django import forms

class SettingsForm(forms.Form):
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Тёмная'),
    ]
    LANG_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'English'),
    ]

    theme = forms.ChoiceField(choices=THEME_CHOICES, required=False)
    language = forms.ChoiceField(choices=LANG_CHOICES, required=False)
    notifications = forms.BooleanField(required=False, label='Уведомления включены')
