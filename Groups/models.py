from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    groupName = models.CharField(max_length=100, null=False, blank=False, default=None)
    purpose = models.CharField(max_length=254, null=False, blank=True, default=None)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.groupName

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "%s" %self.member

    def getGroup(self):
        return self.group

    def getMember(self):
        return self.member

class InviteUser(models.Model):
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_to')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_by')

    def __str__(self):
        return "%s invited you to join %s" %(self.sent_by, self.group)
