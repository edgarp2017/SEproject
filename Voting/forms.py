from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.contrib.auth.models import User

from Users.models import AcceptedUser
from .models import VoteSU
from .models import UserVote
from Groups.models import Group

class VoteSUForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('request')
        super(VoteSUForm, self).__init__(*args,**kwargs)
        self.fields['vote_for'].queryset = AcceptedUser.objects.filter(is_VIP=True).exclude(user=self.user)

    vote_for = forms.ModelChoiceField(queryset=None)

    class Meta:
        fields = [
            'vote_for',
        ]

    def save(self):
        data = self.cleaned_data
        try:
            vote = VoteSU.objects.get(vote_for=data['vote_for'].user)
            vote.voteGiven()
            vote.voters.add(self.user)
            vote.save()
        except ObjectDoesNotExist:
            vote = VoteSU.objects.create(vote_for=data['vote_for'].user, count=1)
            vote.voters.add(self.user)
            vote.save()

        self.checkVotes()

    def checkUserVoted(self, user):
        votes = VoteSU.objects.all()
        for instance in votes:
            voters = instance.voters.all()
            for voter in voters:
                if voter.username == self.user.username:
                    return True
        return False

    def checkVotes(self):
        totalVotes = 0

        votes = VoteSU.objects.all()
        for instance in votes:
            totalVotes += instance.count

        if AcceptedUser.objects.filter(is_VIP=True).count() == totalVotes:
            newSU = VoteSU.objects.all().order_by('-count')[0]
            user = AcceptedUser.objects.get(user=newSU.vote_for)
            user.is_VIP = False
            user.is_SU  = True
            user.save()

class UserVoteForm(forms.ModelForm):

    class Meta:
        model = UserVote
        fields = [
            'member',
            'voteType',
        ]

    options = [('1', 'Praise'), ('2','Warn')]
    member = forms.MultipleChoiceField(choices=[], label='Member Name', required=False,
                                       widget=forms.SelectMultiple(attrs={
                                        'class':'form-control'
                                        }))

    voteType = forms.CharField(label='Are you praising or warning?', widget=forms.RadioSelect(choices=options))


    otherMember = forms.CharField(label='Someone else?', max_length=100, required=False,
                                  widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder':'Did we miss someone?'
                                    }))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('request',None)
        self.group = kwargs.pop('group',None)
        super(UserVoteForm, self).__init__(*args, **kwargs)
        currentGroup = Group.objects.get(name=self.group)
        members = currentGroup.members.all()
        currentGroupMembers = User.objects.filter(username__in=list(members)).exclude(username=self.user)
        self.fields['member'].choices = [(member,member) for member in currentGroupMembers]


    def checkVoteType(self):
        data = self.cleaned_data
        return(data['voteType'])


