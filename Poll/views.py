from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreatePollForm
from .models import Poll


def poll(request):
    polls = Poll.objects.all()
    form = CreatePollForm()
    context = {'polls':polls}
    return render(request, 'poll/pollhome.html', context)

def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['question'])
            form.save()
            return redirect('/poll')
    else:

        form = CreatePollForm()

    context = {'form':form}
    return render(request, 'poll/create.html', context)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':
        option = request.POST['poll']
        print(request.POST['poll'])

        if option == 'option1':
            print("here")
            poll.ans_one_votes += 1
        elif option == 'option2':
            poll.ans_two_votes += 1
        elif option == 'option3':
            poll.ans_three_votes += 1
        else:
            HttpResponse(400, 'Invalid Form')

        poll.save()

        return redirect('Result',poll.id)

    context = {'poll':poll}
    return render(request, 'poll/vote.html', context)

def result(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {'poll':poll}
    return render(request, 'poll/result.html', context)
