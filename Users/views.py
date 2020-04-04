from django.shortcuts import render, redirect
from django.contrib.auth import views
from django.contrib.auth.models import User
from .forms import (
    SignUpForm,
    NewUserForm,
)

class LoginView(views.LoginView):
    template_name = 'Users/login.html'

def SignUpView(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return redirect('/users')
    return render(request, 'users/signup.html', {'form': form})

def NewUserView(request):
    users = User.objects.all().filter(is_active=False)
    form = NewUserForm(request.POST)
    if form.is_valid():
        user.is_active = False
        user.save()
        return redirect('/users')
    return render(request, 'Users/newusers.html', {'form': form, 'users': users})