from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import VoteSUForm
from .models import VoteSU
from Users.models import AcceptedUser

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
def uservote(request):
    return render(request,'teamup/home.html')
