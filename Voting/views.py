from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import VoteSU, UserVote, VoteType, Vote
from .forms import VoteSUForm, UserVoteForm, VoteTypeForm, VoteForm
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

def uservote(request,pk):
    pass
    return render(request, 'Voting/uservote.html')
    
@login_required(login_url="/login")
def VoteFormView(request, grouppk, votepk):
    return render(request, 'Voting/response.html', {'group': group, 'votes':votes})

@login_required(login_url="/login")
def StartVoteView(request, pk):
    group = Group.objects.get(pk=pk)
    form = VoteTypeForm(request.POST, request=request.user, group=group)
    if form.is_valid():
        if form.checkExist():
            messages.success(request, 'Vote Exist, Try again later!')
        else:
            startVote = form.save(commit=False)
            startVote.group = group
            startVote.save()
            messages.success(request, 'Vote Started!')

    return render(request, 'Voting/start_vote.html', {'form':form})

@login_required(login_url="/login")
def GroupMemberVoteView(request, pk):
    group = Group.objects.get(pk=pk)
    voteTypeObject = VoteType.objects.get(group=group)
    form = VoteForm(request.POST, request=request.user, group=group)

    if form.is_valid():
        if form.checkVoted():
            messages.success(request, 'You already voted!')
        else:
            voteObject = Vote.objects.get(vote=voteTypeObject)
            voteObject.voters.add(request.user)
            answer = form.getResponse()
            if answer == '1':
                voteObject.yes_count += 1
            else:
                voteObject.no_count += 1
            voteObject.save()
            messages.success(request, 'Your vote has been saved!')

    return render(request, 'Voting/votes.html', {'group': group, 'votes':voteTypeObject, 'form':form})