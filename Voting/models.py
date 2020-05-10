from django.db import models
from django.contrib.auth.models import User

from Groups.models import Group
from Users.models import AcceptedUser

class VoteSU(models.Model):
    vote_for = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vote_for")
    count = models.IntegerField(default=1)
    voters = models.ManyToManyField(User, related_name="voters")

    def __str__(self):
        return "%s has %s votes" %(self.vote_for, self.count)

    def voteGiven(self):
        self.count += 1


class UserVote(models.Model):
    pCount = models.IntegerField(default=0)
    wCount = models.IntegerField(default=0)
    kickCount = models.IntegerField(default=0)
    voterName = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %d votes' % (self.voterName, self.pCount + self.wCount)

    def praise(self):
        self.pCount += 1

    def warn(self):
        self.wCount += 1

    #Needs refinement
    @classmethod
    def bulk_votes(cls, voterName):
        with transaction.atomic():
            for voterName in voterNames:
                if len(voterName) == 0:
                    continue

                if UserVote.objects.filter(voterName=voterName).exist():
                    UserVote.objects.filter(voterName=voterName).update(wCount=models.F('wCount') + 1)

                else:
                    UserVote.objects.create(voterName=voterName, count=1)
