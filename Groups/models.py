from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=254)
    members = models.ManyToManyField(User, related_name='members')

    def __str__(self):
        return self.name

class InviteUser(models.Model):
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_to')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_by')

    def __str__(self):
        return "%s invited you to join %s" %(self.sent_by, self.group)

class RejectedInviteMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group')
    invite_rejected_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invite_rejected_by')
    message = models.CharField(max_length=100)

    def __str__(self):
        return "%s rejected invite for %s group" %(self.invite_rejected_by, self.group)