from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Application(models.Model):
    firstName = models.CharField(max_length=50, null=False)
    lastName = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=254, null=False)
    interest = models.TextField(null=False)
    credential = models.TextField(null=False)
    reference = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.firstName+ ' ' + self.lastName

class AcceptedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_OU = models.BooleanField(default=True)
    is_VIP = models.BooleanField(default=False)
    is_SU = models.BooleanField(default=False)
    rep_score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class RejectedUser(models.Model):
    user = models.CharField(max_length=50)
    #rejectedUserID = models.IntegerField(null=True)
    
    def __str__(self):
        return self.user
        