from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, UsersWaitingResponse, AcceptedUser, RejectedUser
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

    def ApplicationInfo(self,user):
        data = self.cleaned_data
        application = Application.objects.create(user=user, firstName=data['firstName'], lastName=data['lastName'],
        email=data['email'], interest=data['interest'], credential=data['credential'], reference=data['reference'])

class NewUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=UsersWaitingResponse.objects.all())
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
            #remove from UsersWaitingResponse 
            removeUser = UsersWaitingResponse.objects.get(user=uid)
            removeUser.delete()
            #enable the account for it can login
            user.is_active = True
            user.save()
            #Add user to AcceptedUser
            accept = AcceptedUser.objects.create(user=user)
        else:
            rejected = RejectedUsers.objects.create(user=data['user'])
            user.delete()
            rejected.save()
         