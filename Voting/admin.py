from django.contrib import admin

from .models import VoteSU, VoteType, Vote, WarnList

admin.site.register(VoteSU)
admin.site.register(VoteType)
admin.site.register(Vote)
admin.site.register(WarnList)