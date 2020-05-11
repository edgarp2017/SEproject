from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
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
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    voteType = models.CharField(max_length=10)
    member = models.CharField(max_length=254)

    def __str__(self):
        return '%s: %d votes' % (self.group, self.pCount + self.wCount)

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

class VoteType(models.Model):
    PRIASE = 'priase'
    WARN = 'warn'
    KICK = 'kick'
    TYPE = [
        (PRIASE, 'priase'),
        (WARN, 'warn'),
        (KICK, 'kick')
    ]
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10,
        choices=TYPE,
        default=PRIASE)

    def __str__(self):
        return "Vote on %s for %s" %(self.user, self.vote_type)

class Vote(models.Model):
    vote = models.OneToOneField(VoteType, on_delete=models.CASCADE)
    yes_count = models.IntegerField(default=0)
    no_count = models.IntegerField(default=0)
    voters = models.ManyToManyField(User)

    def __str__(self):
        return "%s: %s yes, %s no" %(self.vote, self.yes_count, self.no_count)

    def updateYes(self):
        self.yes_count += 1

    def updateNo(self):
        self.no_count += 1

@receiver(post_save, sender=VoteType)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Vote.objects.create(vote=instance)