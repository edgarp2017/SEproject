from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
# def test(request):
#     print("hello")
#     return render(request, 'login.html', {'title': 'Home'})
def home(request):
    return render(request, 'Navbar.html')
