from django.contrib import admin
from .models import Application, UsersWaitingResponse, AcceptedUser, RejectedUser

admin.site.register(Application)
admin.site.register(UsersWaitingResponse)
admin.site.register(AcceptedUser)
admin.site.register(RejectedUser)