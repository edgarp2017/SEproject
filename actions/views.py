from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import complaint
from .forms import ActionForm, SUActionForm


def actions(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ActionForm(request.POST, request.FILES, request=request)
        # check whether it's valid:
        if form.is_valid():
                if 'praise' in request.POST:
                    if request.user.is_anonymous:
                        messages.error(request, 'Must be logged in to send a compliment')
                        return redirect('/login')
                    if (request.POST.get('username')):
                        form.compliment()
                        messages.success(request, 'Compliment Has Been Sent')
                    else:
                        messages.error(request, 'Please Select a User to Compliment')


                if 'complaint' in request.POST:
                    if (request.POST.get('username') and request.POST['group']):
                        messages.error(request, 'Please Select Either User or Group Not Both!')
                    
                    elif (request.POST.get('username')):
                        form.complaint()
                        messages.success(request, 'Complaint Has Been Filed')

                    elif (request.POST.get('group')):
                        form.complaint()
                        messages.success(request, 'Complaint Has Been Filed')
                        
                    else:
                        messages.error(request, 'Please Select Either User or Group!')
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ActionForm(request.POST, request.FILES, request=request)

    return render(request, 'actions/action.html', {'form': form})

def SUactions(request):
    complaints = complaint.objects.order_by('id')
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SUActionForm(request.POST)
        # check whether it's valid:
       
        if form.is_valid():
            if 'resolved' in request.POST:
                form.Resolved(request.POST.get('resolved'))
                messages.success(request, 'Complaint Has Been Resolved')

            else:
                if (request.POST.get('username') and request.POST['group']):
                    messages.error(request, 'Please Select Either User or Group Not Both!')

                elif not(request.POST.get('username') and request.POST['group']):
                    messages.error(request, 'Please Select Either User or Group!')

                else:
                    if 'deduct' in request.POST:
                        form.Deduct()
                        messages.success(request, 'Points Have Been Deducted!')

                    if 'delete' in request.POST:
                        form.Delete()
                        messages.success(request, 'Entity Has Been Deleted')

            

        # process the data in form.cleaned_data as required
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')

    form = SUActionForm(request.POST)
    context = {'complaints' : complaints,'form': form}
    return render(request, 'actions/SUaction.html', context)