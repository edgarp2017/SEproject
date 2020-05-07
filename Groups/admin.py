from django.contrib import admin
from .models import Group, GroupMember, InviteUser

admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(InviteUser)
