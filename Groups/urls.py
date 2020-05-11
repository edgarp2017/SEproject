from django.urls import path

from . import views
from Post.views import PostView

app_name = "Groups"

urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', views.groups, name='groups'),
    path('create/', views.create, name='makegroup'),
    path('groups/<pk>', views.GroupDetail.as_view(), name='group_detail'),
    path('groups/<pk>/post', PostView, name='new_post'),
    path('groups/<pk>/invite/', views.InviteUserFormView, name='invite'),
    path('groups/<pk>/rejectmessages', views.RejectMessagesView, name='reject_messages'),
    path('my_invites/', views.UserInvites, name='my_invites'),
]
