from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
# def test(request):
#     print("hello")
#     return render(request, 'login.html', {'title': 'Home'})
def poll(request):
    contest = {}
    return render(request, 'Navbar.html' context)

def create(request):
    contest = {}
    return render(request, 'Navbar.html', context)

def vote(request, poll_id):
    contest = {}
    return render(request, 'Navbar.html', context)

def result(request, poll_id):
    contest = {}
    return render(request, 'Navbar.html', context)
