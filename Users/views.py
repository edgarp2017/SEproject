from django.contrib import messages
from django.contrib.auth import views
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AcceptRejectForm, BlackBoxMessageForm, AddUserBoxForm
from .models import AcceptedUser, Application, WhiteBox, BlackBox

class NewUserFormView(LoginRequiredMixin, FormView):
    template_name = 'Users/newusers.html'
    form_class = AcceptRejectForm
    success_url = '/user/'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        user = AcceptedUser.objects.get(user=self.request.user)
        if not user.is_SU:
            messages.error(self.request, 'You are not a SU!')
            return redirect('/')
        return super(NewUserFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.getChoice() == False:
            messages.error(self.request, 'Username Already Exists!')
            return redirect('/user/')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.all()
        return context

@login_required(login_url="/login")
def BlackWhiteBoxesView(request):
    blackBoxObject = BlackBox.objects.get(user=request.user)
    blackBoxUsers = blackBoxObject.blackbox.all()

    whiteBoxObject = WhiteBox.objects.get(user=request.user)
    whiteboxUsers = whiteBoxObject.whitebox.all()

    return render(request, 'Users/blackwhite.html', {'blackBoxUsers': blackBoxUsers, 'whiteboxUsers': whiteboxUsers})

@login_required(login_url="/login")
def WhiteBoxView(request):
    form = AddUserBoxForm(request.POST, request=request.user)
    
    if form.is_valid():

        if form.addWhiteBox():
            messages.success(request, 'User Added!')
        else:
            messages.success(request, 'Error, Either user trying to add is in Black Box or White Box!')
        
        return redirect('/user/blackwhite')
    return render(request, 'Users/addtowhitebox.html', {'form':form})

@login_required(login_url="/login")
def BlackBoxView(request):
    form = AddUserBoxForm(request.POST, request=request.user)
    
    if form.is_valid():
        
        if form.addBlackBox():
            messages.success(request, 'User Added!')
        else:
            messages.success(request, 'Error, Either user trying to add is in Black Box or White Box!')
        
        return redirect('/user/blackwhite') 
    return render(request, 'Users/addtoblackbox.html', {'form':form})

@login_required(login_url="/login")
def BlackBoxMessage(request):
    form = BlackBoxMessageForm(request.POST, request=request.user)
    
    if form.is_valid():
        form.updateMessage()
        messages.success(request, 'Message Updated!')
        return redirect('/user/blackwhite') 
    return render(request, 'Users/blackboxmessage.html', {'form':form})