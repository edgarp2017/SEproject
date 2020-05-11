from django.contrib import admin

from .models import VoteSU, UserVote, VoteType, Vote

admin.site.register(VoteSU)
admin.site.register(UserVote)
admin.site.register(VoteType)
admin.site.register(Vote)