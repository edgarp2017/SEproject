from django.urls import path

from . import views
from Post.views import PostView
from Voting.views import StartVoteView, GroupMemberVoteView
from Poll.views import poll, create, vote, result

app_name = "Groups"

urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', views.groups, name='groups'),
    path('create/', views.create, name='makegroup'),
    path('groups/<pk>', views.GroupDetail.as_view(), name='group_detail'),
    path('groups/<pk>/post', PostView, name='new_post'),
    path('groups/<pk>/invite/', views.InviteUserFormView, name='invite'),
    path('groups/<pk>/rejectmessages', views.RejectMessagesView, name='reject_messages'),
    #votes path
    path('groups/<pk>/votes', GroupMemberVoteView, name='votes'),
    path('groups/<pk>/votes/startvote', StartVoteView, name='start_vote'),
    #poll urls
    path('groups/<pk>/viewpolls', poll, name='view_polls'),
    path('groups/<pk>/viewpolls/vote', vote, name='vote_polls'),
    path('groups/<pk>/viewpolls/results', result, name='result_polls'),
    path('groups/<pk>/viewpolls/create', create, name='create_poll'),
    #users personal invites
    path('my_invites/', views.UserInvites, name='my_invites'),
    path('my_invites/<pk>', views.ResponseGroupInvitesView, name='invite_response'),
]
