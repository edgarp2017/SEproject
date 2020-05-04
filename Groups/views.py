from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import GroupForm

# Create your views here.


def home(request):
    return render(request, 'teamup/home.html', {'title': 'Home'})

@login_required(login_url="/login")
def groups(request):
    return render(request, 'teamup/settings.html', {'title': 'settings'})


def login(request):
    return render(request, 'Users/login.html', {'title': 'login'})

def signup(request):
    return render(request, 'Users/signup.html', {'title': 'signup'})

def create(request):
    return render(request, 'teamup/makegroup.html', {'title': 'makegroup'})
