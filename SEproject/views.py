from Users.forms import ApplicationForm
from django.shortcuts import render, redirect
from django.contrib.auth import views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
    
@login_required(login_url="/login")
def Profile(request):
    user = {'User': request.user}
    return render(request, 'profile.html', user)

class LoginView(views.LoginView):
    template_name = 'login.html'

def ApplicationView(request):
    form = ApplicationForm(request.POST)
    if form.is_valid():
        application = form.save()
        return redirect('/')
    return render(request, 'application.html', {'form': form})