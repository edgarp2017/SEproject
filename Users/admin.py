from django.contrib import admin
from .models import Application, AcceptedUser, BlackList

admin.site.register(Application)
admin.site.register(AcceptedUser)
admin.site.register(BlackList)