from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from Users.models import AcceptedUser
from .models import VoteSU
from .models import UserVote
from Groups.models import GroupMember

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


class UserVoteForm(forms.Form):
    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         print(self.user)
         super(UserVoteForm, self).__init__(*args, **kwargs)
         self.fields['voteOption'].choices = GroupMember.objects.filter(member=self.user)
         print(GroupMember.objects.filter(member=self.user).exclude(member=self.user))
         print(self.user)
    voteOption = forms.MultipleChoiceField(choices=[], label='Vote Name', required=False,
                                           widget=forms.SelectMultiple(attrs={
                                            'class':'form-control'
                                            }))
    otherMember = forms.CharField(label='Somone else?', max_length=100, required=False,
                                  widget=forms.TextInput(
                                    attrs={
                                    'class':'form-control',
                                    'placeholder':'Did we miss a member?'
                                    }))
        #if this fails try to loop through members as [(voterName,voterName) for groupmembers in groupmember]
