from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, AcceptedUser, RejectedUser
from .choices import RESPONSE_CHOICES
from django.core.exceptions import ObjectDoesNotExist

class ApplicationForm(forms.ModelForm):
    reference = forms.ModelChoiceField(queryset=User.objects.all())
    class Meta:
        model = Application
        fields = [
            'email',
            'firstName',
            'lastName',
            'interest',
            'credential',
            'reference',
        ]

class AcceptRejectForm(forms.Form):
    application = forms.ModelChoiceField(queryset=Application.objects.all())
    response = forms.ChoiceField(choices=RESPONSE_CHOICES)

    class Meta:
       fields = [
           'application',
           'response'
       ]