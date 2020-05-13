from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Application, AcceptedUser, RejectedUser, BlackList, BlackBox, WhiteBox, Appeal
from .choices import RESPONSE_CHOICES

class ApplicationForm(forms.ModelForm):
    reference = forms.ModelChoiceField(queryset=AcceptedUser.objects.all().filter(is_SU=False))
    
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

    def checkBlackList(self):
        '''This function checks if email is black listed'''
        data = self.cleaned_data
        try:
            BlackList.objects.get(email=data['email'])
        except ObjectDoesNotExist:
            return False
        return True

    def checkApplicationExist(self):
        '''This function checks if the email has already applied and is waitng for response'''
        data = self.cleaned_data
        try:
            Application.objects.get(email=data['email'])
        except ObjectDoesNotExist:
            return False
        return True


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
        username = data['username']

        if data['response'] == "1":
            if User.objects.filter(username=username).exists():
                return False
            else:
                self.acceptApplication(data['username'], data['password'], application)
        else:
            self.rejectApplication(application.email)

        application.delete()
        return True

    def acceptApplication(self, username, password, application):
        '''Will email username and password also create user and accepteduser'''
        user = User.objects.create_user(username, password=password, email=application.email, 
        first_name=application.firstName, last_name=application.lastName)
        user.save()
        AcceptedUser.objects.create(user=user, reference=application.reference)
        status = 'new user was created'

        #send out email if accepted
        html_message = render_to_string('AcceptEmail.html', {'username': username, 'password':password})
        plain_message = strip_tags(html_message)
        
        send_mail('Welcome to TeamUp', plain_message, 'sender@example.com', [application.email], html_message=html_message) #action of sending email
     
        
    def rejectApplication(self, email):
        '''Function will handle rejection of application
        if it is first time it will be added to rejected DB
        otherwise added to Blacklist DB'''
        if(self.checkRejected(email)):
            #adds to blacklist only if it was rejected before
            BlackList.objects.create(email=email)
            html_message = render_to_string('BlackListEmail.html', {})
            plain_message = strip_tags(html_message)
            send_mail('TeamUp: BLACKLISTED', plain_message, 'sender@example.com', [email], html_message=html_message) #action of sending email
        else:
            RejectedUser.objects.create(email=email)
            html_message = render_to_string('RejectionEmail.html', {})
            plain_message = strip_tags(html_message)
            send_mail('TeamUp: Sorry', plain_message, 'sender@example.com', [email], html_message=html_message) #action of sending email

    def checkRejected(self, email):
        '''This function checks if Application has been rejected before'''
        try:
            RejectedUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return False
        return True

class BlackBoxMessageForm(forms.Form):
    
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('request')
        super(BlackBoxMessageForm, self).__init__(*args,**kwargs)

    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        fields = [
            'message'
        ]    

    def updateMessage(self):
        data = self.cleaned_data

        userBlackBox = BlackBox.objects.get(user=self.user)
        userBlackBox.message = data['message']
        userBlackBox.save()

class AddUserBoxForm(forms.Form):

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('request')
        super(AddUserBoxForm, self).__init__(*args,**kwargs)
        self.fields['user'].queryset = User.objects.filter(username__in=list(AcceptedUser.objects.filter(is_OU=True).exclude(user=self.user)))

    user = forms.ModelChoiceField(queryset=None)

    class Meta:
        fields = [
            'user'
        ] 

    def addBlackBox(self):
        data = self.cleaned_data
        blackBoxObject = BlackBox.objects.get(user=self.user)

        if self.checkSelectedUser():
            return False
        else:
            blackBoxObject.blackbox.add(data['user'])
            blackBoxObject.save()
            return True

    def addWhiteBox(self):
        data = self.cleaned_data
        whiteBoxObject = WhiteBox.objects.get(user=self.user)
        
        if self.checkSelectedUser():
            return False
        else:
            whiteBoxObject.whitebox.add(data['user'])
            whiteBoxObject.save()
            return True

    def checkSelectedUser(self):
        data = self.cleaned_data
        blackBoxObject = BlackBox.objects.get(user=self.user)
        whiteBoxObject = WhiteBox.objects.get(user=self.user)
        blackBoxUsers = blackBoxObject.blackbox.all()
        whiteBoxUsers = whiteBoxObject.whitebox.all()

        for instance in blackBoxUsers:
            if instance.username == data['user'].username:
                return True

        for instance in whiteBoxUsers:
            if instance.username == data['user'].username:
                return True

class AppealForm(forms.ModelForm):
    reference = forms.ModelChoiceField(queryset=AcceptedUser.objects.all().filter(is_SU=False))
    class Meta:
        model = Appeal
        fields = [
            'email',
            'firstName',
            'lastName',
            'reference'
        ]

    def checkAppealNeeded(self):
        data = self.cleaned_data
        try:
            RejectedUser.objects.get(email=data['email'])
        except ObjectDoesNotExist:
            return False
        return True

    def checkBlackListed(self):
        data = self.cleaned_data
        try:
            BlackList.objects.get(email=data['email'])
        except ObjectDoesNotExist:
            return False
        return True


class AppealResposneForm(forms.Form):
    appeal = forms.ModelChoiceField(queryset=Appeal.objects.all())
    response = forms.ChoiceField(choices=RESPONSE_CHOICES)
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
       fields = [
           'appeal',
           'response',
           'username',
           'password'
       ]
    
    def getChoice(self):
        data = self.cleaned_data
        appeal = data['appeal']
        username = data['username']

        if data['response'] == "1":
            if User.objects.filter(username=username).exists():
                return False
            else:
                self.acceptApplication(data['username'], data['password'], appeal)
        else:
            self.rejectApplication(appeal.email)

        appeal.delete()
        return True

    def acceptApplication(self, username, password, appeal):
        '''Will email username and password also create user and accepteduser'''
        user = User.objects.create_user(username, password=password, email=appeal.email, 
        first_name=appeal.firstName, last_name=appeal.lastName)
        user.save()
        AcceptedUser.objects.create(user=user, reference=appeal.reference)
        status = 'new user was created'

        #send out email if accepted
        html_message = render_to_string('AcceptEmail.html', {'username': username, 'password':password})
        plain_message = strip_tags(html_message)
        
        send_mail('Welcome to TeamUp', plain_message, 'sender@example.com', [application.email], html_message=html_message) #action of sending email

        
    def rejectApplication(self, email):
        BlackList.objects.create(email=email)
        html_message = render_to_string('BlackListEmail.html', {})
        plain_message = strip_tags(html_message)
        send_mail('TeamUp: BLACKLISTED', plain_message, 'sender@example.com', [email], html_message=html_message) #action of sending email
       
    