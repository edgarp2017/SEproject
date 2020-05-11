from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreatePollForm
from .models import Poll
from Groups.models import Group
from django.core.exceptions import ObjectDoesNotExist


def poll(request, pk):
    group = Group.objects.get(pk=pk)

    try:
        polls = Poll.objects.get(Group=pk)
    except ObjectDoesNotExist:
        polls = None
    context = {'polls':polls,
                'group':group}
    return render(request, 'poll/pollhome.html', context)

def create(request,pk):
    group = Group.objects.get(pk=pk)
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['question'])
            c: create = form.save(commit=False)
            c.Group = group
            c.save()
            c.Voter.add(request.user)
            c.save()
            return redirect('/groups/%s/viewpolls' %group.pk)
    else:

        form = CreatePollForm()

    context = {'form':form}
    return render(request, 'poll/create.html', context)

def vote(request,pk):
    group = Group.objects.get(pk=pk)
    poll = Poll.objects.get(Group=pk)

    if request.method == 'POST':
        option = request.POST['poll']
        print(request.POST['poll'])

        if option == 'option1':
            poll.ans_one_votes += 1
        elif option == 'option2':
            poll.ans_two_votes += 1
        elif option == 'option3':
            poll.ans_three_votes += 1
        else:
            HttpResponse(400, 'Invalid Form')

        poll.save()

        return redirect('/groups/%s/viewpolls' %group.pk)

    context = {'poll':poll,
                'group':group}

    return render(request, 'poll/vote.html', context)

def result(request, pk):
    poll = Poll.objects.get(Group=pk)
    context = {'poll':poll}
    return render(request, 'poll/result.html', context)
