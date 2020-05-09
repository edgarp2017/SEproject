from django.db import models
from django.contrib.auth.models import User

from Users.models import AcceptedUser

class VoteSU(models.Model):
    vote_for = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vote_for")
    count = models.IntegerField(default=1)
    voters = models.ManyToManyField(User, related_name="voters")

    def __str__(self):
        return "%s has %s votes" %(self.vote_for, self.count)

    def voteGiven(self):
        self.count += 1