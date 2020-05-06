from django import forms
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist

from .models import Group, InviteUser

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['groupName',
            'purpose']

    def checkExist(self):
        data = self.cleaned_data
        try:
            Group.objects.get(groupName=data['groupName'])
        except ObjectDoesNotExist:
            return False
        return True


class GroupInviteForm(ModelForm):
    class Meta:
        model = InviteUser
        fields = [
            'sent_to',
        ]
