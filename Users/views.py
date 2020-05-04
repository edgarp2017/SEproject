from django.shortcuts import render, redirect
from django.contrib.auth import views
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from .forms import (
    NewUserForm,
)
from .models import (
    UsersWaitingResponse,
    User
)

class NewUserFormView(FormView):
    template_name = 'Users/newusers.html'
    form_class = NewUserForm
    success_url = '/users/'

    def form_valid(self, form):
        form.acceptRejectFunction()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().filter(is_active=False)
        context['usersWaiting'] = UsersWaitingResponse.objects.all()
        return context

def ProfileView(request, username):
    user = User.objects.get(username=username)
    return render(request, 'Users/profile.html', {"user":user})
