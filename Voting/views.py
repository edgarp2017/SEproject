from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import VoteSU, UserVote
from .forms import VoteSUForm, UserVoteForm
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
def uservote(request,pk):
    group = Group.objects.get(pk=pk)
    form = UserVoteForm(request.POST, request=request.user, group=group)
    if request.method == 'POST':
        if form.is_valid():
            v: vote = form.save(commit=False)
            v.group = group
            if form.cleaned_data['voteType'] == '1':
                v.pCount += 1
                v.voteType = 1

            if form.cleaned_data['voteType'] == '2':
                v.wCount += 1
                v.voteType = 2

            v.save()
            print(v.wCount)
            message = 'Thank you for voting!'
    if request.method == 'GET':
        message = ''

    #form = UserVoteForm()

    context = {
        'form':form,
        'message': message
    }

    return render(request, 'Voting/uservote.html', context)
