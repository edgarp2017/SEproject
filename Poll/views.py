from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreatePollForm
from .models import Poll
from Groups.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login")
def poll(request, pk):
    group = Group.objects.get(pk=pk)

    try:
        polls = Poll.objects.get(Group=pk)
    except ObjectDoesNotExist:
        polls = None
    context = {'polls':polls,
                'group':group}

    if request.method == 'POST':
        if not polls == None:
            polls.delete()
            messages.success(request, "Poll has been deleted successfully")
            return redirect('/groups/%s/viewpolls' %group.pk)


    return render(request, 'poll/pollhome.html', context)

@login_required(login_url="/login")
def create(request,pk):

    try:
        polls = Poll.objects.get(Group=pk)
    except ObjectDoesNotExist:
        polls = None

    group = Group.objects.get(pk=pk)
    form = CreatePollForm(request.POST,request=request.user, group=group)

    if not polls == None:
        messages.error(request, 'There is an active poll already')
        return redirect('/groups/%s/viewpolls' %group.pk)

    if request.method == 'POST':
        if form.is_valid():
            print(form.cleaned_data['question'])
            c: create = form.save(commit=False)
            c.Group = group
            c.save()
            return redirect('/groups/%s/viewpolls' %group.pk)
    else:

        form = CreatePollForm()

    context = {'form':form}
    return render(request, 'poll/create.html', context)

@login_required(login_url="/login")
def vote(request,pk):
    group = Group.objects.get(pk=pk)
    poll = Poll.objects.get(Group=pk)
    user = request.user
    voted = False
    form = CreatePollForm(request.POST, request=request.user, group=group)
    members = group.members.all().count()

    voters = poll.Voter.all()
    votersCount = poll.Voter.all().count()
    print(votersCount)
    print(members)

    for vote in voters:
        if vote.username == user.username:
            voted = True


    if request.method == 'POST':
        option = request.POST['poll']
        if voted == True:
            messages.error(request, 'You already voted!')
            return redirect('/groups/%s/viewpolls' %group.pk)

        poll.Voter.add(request.user)

        if option == 'option1':
            poll.ans_one_votes += 1
        elif option == 'option2':
            poll.ans_two_votes += 1
        elif option == 'option3':
            poll.ans_three_votes += 1
        else:
            HttpResponse(400, 'Invalid Form')

        poll.save()

        votersCount +=1

        if members == votersCount:
            form.delete()
            messages.success(request, 'The Results of the poll have been posted!')
            return redirect('/groups/%s' %group.pk)

        return redirect('/groups/%s/viewpolls' %group.pk)

    context = {'poll':poll,
                'group':group}

    return render(request, 'poll/vote.html', context)

@login_required(login_url="/login")
def result(request, pk):
    poll = Poll.objects.get(Group=pk)
    context = {'poll':poll}
    return render(request, 'poll/result.html', context)
