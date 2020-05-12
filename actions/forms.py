from django import forms
from django.contrib.auth.models import User
from Users.models import AcceptedUser
from Groups.models import Group
from .models import compliment, complaint

class ActionForm(forms.Form):
    #your_name = forms.CharField(label='Your name', max_length=100)
    def __init__(self,*args,**kwargs):
        self.request= kwargs.pop('request')
        super(ActionForm, self).__init__(*args,**kwargs)
        try: 
            self.fields['username'].queryset = AcceptedUser.objects.exclude(user = self.request.user).filter(is_SU=False)
        except:
            self.fields['username'].queryset = AcceptedUser.objects.filter(is_SU=False)
        
        

    # Use any form fields you need, CharField for simplicity reasons
    username = forms.ModelChoiceField(queryset=None,required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all(),required=False)
    email = forms.CharField(required = False)
    firstName = forms.CharField(required = False)
    lastName = forms.CharField(required = False)
    reason = forms.CharField(required = False, widget=forms.Textarea)
    
    
    class Meta:
       fields = [
           'username',
           'group',
           'reason',
            'firstName',
            'lastName',
            'email'
       ]

    def compliment(self):
        data = self.cleaned_data
        user = data['username']
        print(user)
        new_praise, created = compliment.objects.update_or_create(user = user)
        if created == False:
            new_praise.praises+=1
            if new_praise.praises >= 3:
                #increase rep
                username = User.objects.get(username=user)
                userPraised = AcceptedUser.objects.get(user=username)
                userPraised.rep_score+=1
                userPraised.save()
                new_praise.praises = 0
        new_praise.save()


    def complaint(self):
        data = self.cleaned_data

        if data['group'] == None: # if user is complained on
            user = User.objects.get(username=data['username'])
            guiltyUser = user.username
            new_complaint, created = complaint.objects.update_or_create(email = data['email'], firstName = data['firstName'], lastName = data['lastName'],guiltyUser = guiltyUser, guiltyGroup = None, Reason = data['reason'] )
            new_complaint.save()

        if data['username'] == None: # if group is complained on
            group = Group.objects.get(name=data['group'])
            guiltyGroup = group.name
            new_complaint, created = complaint.objects.update_or_create(email = data['email'], firstName = data['firstName'], lastName = data['lastName'],guiltyUser = None, guiltyGroup = guiltyGroup, Reason = data['reason'] )
            new_complaint.save()

class SUActionForm(forms.Form):
    #complaints = forms.ModelChoiceField(queryset=complaint.objects.all())
    username = forms.ModelChoiceField(queryset=AcceptedUser.objects.all().filter(is_SU=False),required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all(),required=False)
    deduction = forms.IntegerField(help_text='Enter the Points to Deduct for the select User or Group',required=False)
    def Deduct(self):
        data = self.cleaned_data
        
        if data['username'] == None: # if group is complained on
            group = Group.objects.get(name=data['group'])
            for user in group.members.all():
                guiltyUser = AcceptedUser.objects.get(user=user)
                guiltyUser.rep_score-=data['deduction']
                guiltyUser.save()



        if data['group'] == None: # if user is comlained on
            user = User.objects.get(username=data['username'])
            guiltyUser = AcceptedUser.objects.get(user=user)
            guiltyUser.rep_score-=data['deduction']
            guiltyUser.save()

    def Delete(self):
        data = self.cleaned_data

        if data['username'] == None: # if group is complained on
            group = Group.objects.get(name=data['group'])
            group.delete()

        if data['group'] == None: # if user is comlained on
            user = User.objects.get(username=data['username'])
            user.delete()

    def Resolved(self,id):
        fixed_complaint = complaint.objects.get(id = id)
        fixed_complaint.delete()

