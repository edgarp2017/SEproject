from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

class Application(models.Model):
    email = models.EmailField(max_length=254, null=False)
    firstName = models.CharField(max_length=50, null=False)
    lastName = models.CharField(max_length=50, null=False)
    interest = models.CharField(max_length=100, null=False)
    credential = models.CharField(max_length=100, null=False)
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

class BlackList(models.Model):
    email = models.EmailField(max_length=254, null=False)
    
    def __str__(self):
        return self.email

class RejectedUser(models.Model):
    email = models.EmailField(max_length=254, null=False)
    
    def __str__(self):
        return self.email
        