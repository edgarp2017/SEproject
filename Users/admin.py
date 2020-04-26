from django.contrib import admin
from .models import Application, UsersWaitingResponse, AcceptedUsers, RejectedUsers

admin.site.register(Application)
admin.site.register(UsersWaitingResponse)
admin.site.register(AcceptedUsers)
admin.site.register(RejectedUsers)