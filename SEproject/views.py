from Users.forms import ApplicationForm
from django.shortcuts import render, redirect
from django.contrib.auth import views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Users.models import AcceptedUser
from .form import InitialReputationForm 
from Groups.models import GroupMember, InviteUser
    
@login_required(login_url="/login")
def Profile(request):
    ref = AcceptedUser.objects.all().filter(reference=request.user)
    groups = GroupMember.objects.all().filter(member=request.user)
    invites = InviteUser.objects.all().filter(sent_to=request.user)
    user = AcceptedUser.objects.get(user=request.user)

    form = InitialReputationForm(request.POST, request=user)
    role = user.getRole()

    if form.is_valid():
        form.save(role)
        return redirect('/profile/')
        
    return render(request, 'profile.html', {'User': request.user, 'ref': ref, 'form': form, 'groups':groups, 'invites':invites })

class LoginView(views.LoginView):
    template_name = 'login.html'

def ApplicationView(request):
    form = ApplicationForm(request.POST)
    if form.is_valid():
        if (form.checkBlackList()):
            #if user is BlackListed 
            messages.success(request, 'Application Failed, You are Black Listed!')
            return redirect('/')

        if (form.checkApplicationExist()):
            #if user tried to apply again it will prevent them from creating another application
            messages.success(request, 'Application Failed, You Have applied already. Please wait!')
            return redirect('/')
            
        application = form.save()
        messages.success(request, 'Application Submited!')
        return redirect('/')
    return render(request, 'application.html', {'form': form})