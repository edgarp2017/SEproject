from django.contrib import admin
from .models import MyGroup, Vote

# Register your models here.

admin.site.register(MyGroup)
admin.site.register(Vote)