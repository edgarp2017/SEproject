from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    groupName= models.CharField(max_length=100, null=False, blank=False, default=None)
    purpose = models.CharField(max_length=254, null=False, blank=True, default=None)

    def __str__(self):
        return self.groupName

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return ("%s is a member of %s" %(self.member, self.group))

    def getGroup(self):
        return self.group

    def getMember(self):
        return self.member

class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Yes'),
        (2, 'No'),
    )
    #user = models.ManyToManyField(User)
    user_vote = models.IntegerField(choices=VOTE_CHOICES)
    #group = models.OneToOneField(MyGroup, on_delete=models.CASCADE)
    #user_vote_on = models.OneToOneField(User, on_delete=models.CASCADE)

