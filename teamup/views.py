from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return HttpResponse('<h1>HELLO WORLD</h1>')
   # return render(request, 'teamup/home.html', {'title': 'Home'})


def settings(request):
    return HttpResponse('<h1>HELLO WORLD</h1>')
    # return render(request, 'teamup/settings.html', {'title': 'settings'})
