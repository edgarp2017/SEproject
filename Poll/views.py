from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
# def test(request):
#     print("hello")
#     return render(request, 'login.html', {'title': 'Home'})
def poll(request):
    context = {}
    return render(request, 'poll/pollhome.html', context)

def create(request):
    context = {}
    return render(request, 'poll/create.html', context)

def vote(request, poll_id):
    context = {}
    return render(request, 'Navbar.html', context)

def result(request, poll_id):
    context = {}
    return render(request, 'Navbar.html', context)
