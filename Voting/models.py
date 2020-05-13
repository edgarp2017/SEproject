from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

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

class VoteType(models.Model):
    PRIASE = 'priase'
    WARN = 'warn'
    KICK = 'kick'
    SHUTDOWN = 'shutdown'
    TYPE = [
        (PRIASE, 'priase'),
        (WARN, 'warn'),
        (KICK, 'kick'),
        (SHUTDOWN, 'shutdown')
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

class WarnList(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    group =  models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return "%s has been warned in %s group" %(self.user, self.group)

@receiver(post_save, sender=VoteType)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Vote.objects.create(vote=instance)

class ClosedGroups(models.Model):
        group =  models.ForeignKey(Group, on_delete=models.CASCADE)
    

