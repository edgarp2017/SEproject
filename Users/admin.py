from django.contrib import admin
from .models import Application, AcceptedUser, RejectedUser

admin.site.register(Application)

admin.site.register(AcceptedUser)
admin.site.register(RejectedUser)