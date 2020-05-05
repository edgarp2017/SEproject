from django.shortcuts import render, redirect
from django.contrib.auth import views
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AcceptRejectForm
from .models import Application

class NewUserFormView(LoginRequiredMixin, FormView):
    template_name = 'Users/newusers.html'
    form_class = AcceptRejectForm
    success_url = '/user/'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def form_valid(self, form):
        form.acceptRejectFunction()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.all()
        return context
