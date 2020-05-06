from django import forms
from django.forms import ModelForm
from .models import Group, InviteUser

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['groupName',
            'purpose']

class GroupInviteForm(ModelForm):
    class Meta:
        model = InviteUser
        fields = [
            'sent_to',
        ]
