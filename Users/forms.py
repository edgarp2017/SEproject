from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, UsersWaitingResponse, AcceptedUser, RejectedUser
from .choices import RESPONSE_CHOICES
from django.core.exceptions import ObjectDoesNotExist

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
           'response'
       ]

    def acceptRejectFunction(self):
        '''Adds User to either accepted or rejected user list'''
        data = self.cleaned_data
        user = User.objects.get(username=data['user'])
        userID = User.objects.get(username=data['user']).pk
        removeUser = UsersWaitingResponse.objects.get(user=userID)

        if data['response'] == '1':
            #enable the account for it can login
            user.is_active = True
            user.save()
            #Add user to AcceptedUser
            accept = AcceptedUser.objects.create(user=user)

            #remove from UsersWaitingResponse 
            removeUser.delete()
        else:
            if(self.checkRejectedList(str(data['user']))):
                #here will go the code for user to be added to blacklist DB 
                #also need to ask professor if we should block the ip from using the site
                #just removes user from waiting list for now
                removeUser.delete()
                pass
            else:
                #added to rejeceted DB if rejected the first time
                rejected = RejectedUser.objects.create(user=str(data['user']))
                rejected.save()
                #user account gets deleted if the first time being rejected
                user.delete()
    
    def checkRejectedList(self, username):
        try:
            RejectedUser.objects.get(user=username)
        except ObjectDoesNotExist:
            return False
        return True