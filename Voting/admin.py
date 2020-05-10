from django.contrib import admin

from .models import VoteSU
from .models import UserVote

admin.site.register(VoteSU)
admin.site.register(UserVote)
