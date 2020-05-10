from django.contrib import admin
from .models import Application, AcceptedUser, RejectedUser, BlackList, WhiteBox, BlackBox

admin.site.register(Application)
admin.site.register(AcceptedUser)
admin.site.register(BlackList)
admin.site.register(RejectedUser)
admin.site.register(WhiteBox)
admin.site.register(BlackBox)