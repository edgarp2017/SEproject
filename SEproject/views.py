from Users.forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth import views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def SignUpView(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        form.ApplicationInfo(user)
        return redirect('/')
    return render(request, 'signup.html', {'form': form})
    
@login_required(login_url="/login")
def Profile(request):
    user = {'User': request.user}
    return render(request, 'profile.html', user)

class LoginView(views.LoginView):
    template_name = 'login.html'