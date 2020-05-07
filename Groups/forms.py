from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Group, InviteUser, GroupMember
from Users.models import AcceptedUser
from .taboo import words

class GroupForm(forms.ModelForm):
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


class InviteUserForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('request')
        super(InviteUserForm, self).__init__(*args,**kwargs)

        self.fields['group'].queryset = Group.objects.filter(groupName__in=list(GroupMember.objects.filter(member=self.user)))
        self.fields['sent_to'].queryset = User.objects.exclude(username=self.user)

    group = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = InviteUser
        fields = [
            'group',
            'sent_to',
        ]

    def checkMember(self):
        data = self.cleaned_data
        try:
            GroupMember.objects.get(group=data['group'], member=data['sent_to'])
        except ObjectDoesNotExist:
            return False
        return True

    def checkInviteExist(self):
        data = self.cleaned_data
        try:
            InviteUser.objects.get(group=data['group'], sent_to=data['sent_to'])
        except ObjectDoesNotExist:
            return False
        return True