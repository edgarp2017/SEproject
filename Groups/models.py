from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class MyGroup(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=254, null=False, blank=True, default=None)
    groupName= models.CharField(max_length=100, null=False, blank=False, default=None)

    def __str__(self):
        return self.groupName

class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Yes'),
        (2, 'No'),
    )
    user = models.ManyToManyField(User)
    user_vote = models.IntegerField(choices=VOTE_CHOICES)
    group = models.OneToOneField(MyGroup, on_delete=models.CASCADE)
    #user_vote_on = models.OneToOneField(User, on_delete=models.CASCADE) 

