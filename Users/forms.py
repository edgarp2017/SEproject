from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, AcceptedUser, RejectedUser, BlackList
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
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
       fields = [
           'application',
           'response',
           'username',
           'password'
       ]
    
    def getChoice(self):
        data = self.cleaned_data
        application = data['application']
        email = application.getEmail()

        if data['response'] == "1":
            self.acceptApplication(data['username'], data['password'], email)
        else:
            self.rejectApplication(email)

    def acceptApplication(self, username, password, email):
        '''Will email username and password also create user and accepteduser'''
        user = User.objects.create_user(username, password=password, email=email)
        user.save()
        AcceptedUser.objects.create(user=user)

        #send out email if accepted
        
    def rejectApplication(self, email):
        '''Function will handle rejection of application
        if it is first time it will be added to rejected DB
        otherwise added to Blacklist DB'''
        if(self.checkRejected(email)):
            #adds to blacklist only if it was rejected before
            BlackList.objects.create(email=email)
        else:
            RejectedUser.objects.create(email=email)

        

    def checkRejected(self, email):
        '''This function checks if Application has been rejected before'''
        try:
            RejectedUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return False
        return True