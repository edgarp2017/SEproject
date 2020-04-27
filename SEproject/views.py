from Users.forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth import views

def SignUpView(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        form.ApplicationInfo(user)
        return redirect('/users')
    return render(request, 'signup.html', {'form': form})

class LoginView(views.LoginView):
    template_name = 'login.html'