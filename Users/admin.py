from django.contrib import admin
from .models import Application, AcceptedUser, RejectedUser, BlackList

admin.site.register(Application)
admin.site.register(AcceptedUser)
admin.site.register(BlackList)
admin.site.register(RejectedUser)