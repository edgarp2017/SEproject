from django import forms
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import VoteSU, VoteType, Vote, WarnList
from Groups.models import Group
from Users.models import AcceptedUser
from Post.models import Post

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

class VoteTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('request')
        self.group = kwargs.pop('group')
        super(VoteTypeForm, self).__init__(*args, **kwargs)
        members = self.group.members.all()
        self.fields['user'].queryset = User.objects.filter(username__in=list(members))#.exclude(username=self.user)

    user = forms.ModelChoiceField(queryset=None)
    
    class Meta:
        model = VoteType
        fields = [
            'user',
            'vote_type'
        ]

    def checkExist(self):
        data = self.cleaned_data
        try:
            VoteType.objects.get(group=self.group)
        except ObjectDoesNotExist:
            return False
        return True

    def checkOwner(self):
        data = self.cleaned_data
        groupOwner = Group.objects.get(name=self.group).owner

        if ((groupOwner.username == data['user'].username) and (data['vote_type'] != 'priase')):
            return True

        return False

class VoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        self.user = kwargs.pop('request')
        super(VoteForm, self).__init__(*args, **kwargs)

    CHOICES = [
        (1, 'yes'),
        (2, 'no')
    ]
    response = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = Vote
        fields = [
            'response'
        ]

    def checkVoted(self):
        data = self.cleaned_data
        voteObject = VoteType.objects.get(group=self.group)
        voteResponse = Vote.objects.get(vote=voteObject)
        voters = voteResponse.voters.all()
        for vote in voters:
            if vote.username == self.user.username:
                return True
        return False

    def getResponse(self):
        data = self.cleaned_data
        return data['response']

    def getVotes(self):
        groupObject = Group.objects.get(name=self.group)
        membersCount = groupObject.members.all().count()

        voteObject = VoteType.objects.get(group=self.group)
        voteResponse = Vote.objects.get(vote=voteObject)
        votersCount = voteResponse.voters.all().count()
        user = voteObject.user

        if (votersCount == membersCount-1):

            if (voteObject.vote_type == 'priase'):

                if voteResponse.no_count == 0:
                    self.userPointUpdate(user, 1)
                voteObject.delete()

            elif (voteObject.vote_type == 'warn'):

                if voteResponse.no_count == 0:
                    WarnList.objects.create(user=user, group=self.group)
                    count = WarnList.objects.filter(user=user, group=self.group).count()
                    if (count == 3):
                        self.userPointUpdate(user, -5)    
                        groupObject.members.remove(user)
                    voteObject.delete()

            else:

                if voteResponse.no_count == 0:
                    self.userPointUpdate(user, -10)
                    groupObject.members.remove(user)
                voteObject.delete()

            desc = "Results from vote: %s said yes, %s said no. ***Automatic message once vote is over***" %(voteResponse.yes_count, voteResponse.no_count)
            Post.objects.create(group=self.group, title=voteObject, desc=desc, user=self.user)
                
    def userPointUpdate(self, user, amount):
        acceptedUserObject = AcceptedUser.objects.get(user=user)
        acceptedUserObject.updateRep(amount)

        if (acceptedUserObject.rep_score > 0):
            acceptedUserObject.save()