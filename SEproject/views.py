from Users.forms import ApplicationForm
from django.shortcuts import render, redirect
from django.contrib.auth import views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Users.models import AcceptedUser
from .form import InitialReputation 
    
@login_required(login_url="/login")
def Profile(request):
    ref = AcceptedUser.objects.all().filter(reference=request.user, init_rep=False)
    form = InitialReputation(request.POST)
    user = AcceptedUser.objects.get(user=request.user)
    role = user.getRole()
    if form.is_valid():
        form.save(role)
        return redirect('/profile/')
        

    context = {'User': request.user, 'ref': ref, 'form': form }
    return render(request, 'profile.html', context)

class LoginView(views.LoginView):
    template_name = 'login.html'

def ApplicationView(request):
    form = ApplicationForm(request.POST)
    if form.is_valid():
        application = form.save()
        return redirect('/')
    return render(request, 'application.html', {'form': form})