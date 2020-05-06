from django.contrib import admin
from .models import Group, Vote, GroupMember, InviteUser

# Register your models here.

admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(Vote)
admin.site.register(InviteUser)