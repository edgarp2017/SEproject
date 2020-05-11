from django.contrib import admin
from .models import Group, InviteUser, RejectedInviteMessage
admin.site.register(Group)
admin.site.register(InviteUser)
admin.site.register(RejectedInviteMessage)
