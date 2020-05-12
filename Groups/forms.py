from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Group, InviteUser, RejectedInviteMessage
from Users.models import AcceptedUser, WhiteBox, BlackBox
from Post.models import Post

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name',
            'purpose']

    def checkExist(self):
        data = self.cleaned_data
        try:
            Group.objects.get(name=data['name'])
        except ObjectDoesNotExist:
            return False
        return True


class InviteUserForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('request')
        self.group = kwargs.pop('group')
        super(InviteUserForm, self).__init__(*args,**kwargs)
        self.fields['sent_to'].queryset = User.objects.exclude(username=self.user)

    class Meta:
        model = InviteUser
        fields = [
            'sent_to',
        ]

    def checkUserWhiteBox(self):
        data = self.cleaned_data
        inWhiteBox = False
        whiteBoxObject = WhiteBox.objects.get(user=data['sent_to'])
        usersInWhiteBox = whiteBoxObject.whitebox.all()

        for user in usersInWhiteBox:
            if self.user.username == user.username:
                self.group.members.add(data['sent_to'])
                inWhiteBox = True

        return inWhiteBox

    def checkUserBlackBox(self):
        data = self.cleaned_data
        inBlackBox = False
        blackBoxObject = BlackBox.objects.get(user=data['sent_to'])
        usersInBlackBox = blackBoxObject.blackbox.all()

        for user in usersInBlackBox:
            if self.user.username == user.username:
                getMessage = BlackBox.objects.get(user=data['sent_to'])
                RejectedInviteMessage.objects.create(group=self.group, invite_rejected_by=data['sent_to'], 
                message=getMessage.message)
                inBlackBox = True

        return inBlackBox

    def checkMember(self):
        data = self.cleaned_data
        groupObject = Group.objects.get(pk=self.group.pk)
        members = groupObject.members.all()

        for member in members:
            if member.username == data['sent_to'].username:
                return True
        return False

    def checkInviteExist(self):
        data = self.cleaned_data
        try:
            InviteUser.objects.get(group=self.group, sent_to=data['sent_to'])
        except ObjectDoesNotExist:
            return False
        return True

class InviteResponseForm(forms.Form):
    RESPONSE_CHOICES = [
        (1,'Accept'),
        (2, 'Reject'),
    ]

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('request')
        self.group = kwargs.pop('group')
        self.invite = kwargs.pop('invite')
        super(InviteResponseForm, self).__init__(*args,**kwargs)

    response = forms.ChoiceField(choices=RESPONSE_CHOICES)
    message = forms.CharField()

    class Meta:
        fields = [
            'response',
            'message'
        ]
    
    def saveAction(self):
        data = self.cleaned_data
        if data['response'] == '1':
            self.group.members.add(self.user)
            self.group.save()
            return True
        else:
            Post.objects.create(group=self.group, title="Invitation Rejected",
            desc="%s rejected invitation for %s group. The message the user send is %s. The invitation was sent by %s"
            %(self.user, self.group, data['message'], self.invite.sent_by), user=self.user)
            return False