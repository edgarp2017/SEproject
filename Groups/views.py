from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist

from .forms import GroupForm, InviteUserForm, RejectedInviteMessage,InviteResponseForm
from Users.forms import AddUserBoxForm
from .models import Group, InviteUser, EvaluationRep
from Voting.models import ClosedGroups
from Users.models import AcceptedUser
from Post.models import Post


def home(request):
    users = AcceptedUser.objects.filter(is_OU=True).order_by('-rep_score')[:3]
    groups = Group.objects.all()[:3]
    superUsers =  AcceptedUser.objects.filter(is_SU=True)
    return render(request, 'teamup/home.html', {'title': 'Home', 'users': users, 'groups': groups, 'superUsers': superUsers})

def groups(request):
    groups = Group.objects.all()
    return render(request, 'teamup/groups.html', {'title': 'Groups', 'groups': groups})

@login_required(login_url="/login")
def create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            if(form.checkExist()):
                messages.success(request, 'Group already created!')
                return redirect('/create')
            else:
                group = form.save(commit=False)
                group.owner = request.user
                group.save()
                group.members.add(request.user)
                group.save()
                messages.success(request, 'Group created Successfully!')
                return redirect('/groups/%s' %group.pk)
    else:
        form = GroupForm()
        return render(request, 'teamup/makegroup.html', {'form':form})

@login_required(login_url="/login")
def InviteUserFormView(request, pk):
    group = Group.objects.get(pk=pk)
    form = InviteUserForm(request.POST, request=request.user, group=group)
    if form.is_valid():

        if form.checkMember():
            messages.success(request, 'Try again, User is in that group!')
            return redirect('/groups/%s/invite' %pk)
        elif form.checkUserWhiteBox():
            messages.success(request, 'Success, Invitation Send!')
            return redirect('/groups/%s' %pk)
        elif form.checkUserBlackBox():
            messages.success(request, 'Success, Invitation Send!')
            return redirect('/groups/%s' %pk)
        elif form.checkInviteExist():
            messages.success(request, 'User Is Already Invited, Please Wait!')
            return redirect('/groups/%s/invite' %pk)   
        else:
            invite = form.save(commit=False)
            invite.sent_by = request.user
            invite.group = group
            invite.save()
            messages.success(request, 'Success!')
            return redirect('/groups/%s' %pk)

    return render(request, 'teamup/invite.html', {'form': form})

@login_required(login_url="/login")
def UserInvites(request):
    invites = InviteUser.objects.filter(sent_to=request.user)
    return render(request, 'teamup/userinvites.html', {'invites':invites})

@login_required(login_url="/login")

def evaluation(request,pk):
    group = Group.objects.get(pk=pk)
    members = group.members.all()

    context = {'members' : members}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #form = ActionForm(request.POST, request.FILES, request=request)
        # check whether it's valid:
        for member in members:
            rep  = request.POST['rep'+member.username]
            evaluatingUser = request.user.username
            whiteBox = request.POST['whiteBox']
            blackBox = request.POST['blackBox']
            reason = request.POST['reason']
            evaluation, created = EvaluationRep.objects.update_or_create(evaluatingUser = evaluatingUser, repGiven = rep, group = group, member = member, whiteBox = whiteBox, blackBox = blackBox, reason = reason)
            evaluation.create()

        numMems = members.count()
        if (numMems**(numMems-1)==EvaluationRep.objects.filter(group = group)): # checks is everyone has done the evaluation
            print("Do stuff") #From here on the assigned VIP will check the user evaluations and assign Rep and we also might either add to white box here or in the loop.


    return render(request, 'teamup/evaluation.html',context)    

class GroupDetail(generic.DetailView):
    model = Group
    # If the group is a shutdown down group change the template to this
    
    template_name = 'teamup/groupdetail.html'
    
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = Group.objects.get(name=self.object)
        if ClosedGroups.objects.filter(group = group).exists():
            context['shutdown'] = True
        context['members'] = group.members.all()
        context['member'] = self.checkIfMember()
        context['posts'] = Post.objects.filter(group=self.object)
        return context

    def checkIfMember(self):
        if not self.request.user.is_authenticated:
            return False

        group = Group.objects.get(name=self.object)
        members = group.members.all()
        for member in members:
            if self.request.user.username == member.username:
                return True
        return False

@login_required(login_url="/login")
def RejectMessagesView(request, pk):
    group = Group.objects.get(pk=pk)
    messages = RejectedInviteMessage.objects.filter(group=group)
    return render(request, 'teamup/rejectmessages.html', {'messages':messages})

def ResponseGroupInvitesView(request, pk):
    invite = InviteUser.objects.get(pk=pk)
    group = invite.group
    form = InviteResponseForm(request.POST, request=request.user, group=group, invite=invite)

    if form.is_valid():
        invite.delete()
        if form.saveAction():
            messages.success(request, 'Invite Accepted, Enjoy!')
            return redirect('/groups/%s' %group.pk)
        else:
            messages.success(request, 'Invite Rejected!')
            return redirect('/my_invites/')

    return render(request, 'teamup/inviteresponse.html', {'invite':invite, 'form':form})