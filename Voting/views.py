from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from .models import VoteSU, VoteType, Vote
from .forms import VoteSUForm, VoteTypeForm, VoteForm
from Users.models import AcceptedUser
from Groups.models import Group

@login_required(login_url="/login")
def VoteSUFormView(request):
    u = AcceptedUser.objects.get(user=request.user)

    if not u.is_VIP:
        messages.success(request, 'You are not a VIP!')
        return redirect('/')

    form = VoteSUForm(request.POST, request=request.user)

    if form.is_valid():
        if form.checkUserVoted(u):
            messages.success(request, 'You Already voted!')
            return redirect('/vote')
        else:
            vote = form.save()
            messages.success(request, 'Vote submitted!')
            return redirect('/vote')
    return render(request, 'Voting/voteSU.html', {'form': form})

@login_required(login_url="/login")
def StartVoteView(request, pk):
    group = Group.objects.get(pk=pk)
    form = VoteTypeForm(request.POST, request=request.user, group=group)

    isMember = False
    members = group.members.all()
    for member in members:
        if member.username == request.user.username:
            isMember = True

    if form.is_valid():
        if form.checkOwner():
            messages.info(request, 'You Can only praise a group owner!')
            return redirect('/groups/%s/votes' %group.pk)
        elif form.checkExist():
            messages.error(request, 'Vote Exist, Try again later!')
            return redirect('/groups/%s/votes' %group.pk)
        else:
            startVote = form.save(commit=False)
            startVote.group = group
            startVote.save()
            messages.success(request, 'Vote Started!')
            return redirect('/groups/%s/votes' %group.pk)

    return render(request, 'Voting/start_vote.html', {'form':form, 'isMember': isMember, 'group':group})

@login_required(login_url="/login")
def GroupMemberVoteView(request, pk):
    group = Group.objects.get(pk=pk)
    form = VoteForm(request.POST, request=request.user, group=group)

    isMember = False
    members = group.members.all()
    for member in members:
        if member.username == request.user.username:
            isMember = True

    try:
        voteTypeObject = VoteType.objects.get(group=group)
    except ObjectDoesNotExist:
        voteTypeObject = None

    if not voteTypeObject == None:
        vote = VoteType.objects.get(group=group)
        userVotingOn = vote.user
        if userVotingOn.username == request.user.username:
            messages.error(request, "You can't vote since the vote happening is for you!")
            return redirect('/groups/%s' %group.pk)
        

    if form.is_valid():
        if form.checkVoted():
            messages.error(request, 'You already voted!')
        else:
            voteObject = Vote.objects.get(vote=voteTypeObject)
            voteObject.voters.add(request.user)
            answer = form.getResponse()
            if answer == '1':
                voteObject.yes_count += 1
            else:
                voteObject.no_count += 1
            voteObject.save()
            form.getVotes()
            return redirect('/groups/%s' %group.pk)

            messages.success(request, 'Your vote has been saved!')

    return render(request, 'Voting/votes.html', {'group': group, 'vote':voteTypeObject, 'form':form, 'isMember': isMember})
