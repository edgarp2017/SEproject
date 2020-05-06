from django.contrib import admin
from .models import Group, Vote, GroupMember, InviteUser

# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    list_display = ('groupName', 'slug')
    prepopulated_fields = {'slug': ('groupName',)}


admin.site.register(Group, GroupAdmin)
admin.site.register(GroupMember)
admin.site.register(Vote)
admin.site.register(InviteUser)