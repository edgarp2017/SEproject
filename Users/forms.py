from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UsersWaitingResponse, RejectedUsers
from .choices import *

class SignUpForm(UserCreationForm):
    firstName = forms.CharField()
    lastName = forms.CharField()
    email = forms.EmailField()
    interest = forms.CharField()
    credential = forms.CharField()
    reference = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'firstName',
            'lastName',
            'email',
            'interest',
            'credential',
            'reference',
        ]

class NewUserForm(forms.Form):
    user = forms.ChoiceField(choices=getUsers())
    response = forms.ChoiceField(choices=RESPONSE_CHOICES)

    class Meta:
        fields = [
            'user',
            'response',
        ]

    def save(self):
        data = self.cleaned_data
        user = User.objects.get(username=data['user'])
        uid = User.objects.get(username=data['user']).pk

        if data['response'] == '1':
            user.is_active = True
            u = UsersWaitingResponse.objects.get(user=uid)
            u.delete()
            user.save()
        else:
            rejecteduser = RejectedUsers.objects.create(user=data['user'])
            user.delete()
            rejecteduser.save()
         