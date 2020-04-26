from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Application(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=50, default='firstName', null=False)
    lastName = models.CharField(max_length=50, default='lastName', null=False)
    email = models.EmailField(max_length=254, null=False, default='email@email.com')
    interest = models.TextField(default='My interest are', null=False)
    credential = models.TextField(default='My credentials are', null=False)
    reference = models.CharField(max_length=50, null=False, default='Name')

    def __str__(self):
        return self.user.username

class UsersWaitingResponse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class AcceptedUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_OU = models.BooleanField(default=True)
    is_VIP = models.BooleanField(default=False)
    is_SU = models.BooleanField(default=False)
    rep_score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class RejectedUsers(models.Model):
    user = models.CharField(max_length=50)

    def __str__(self):
        return self.user

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UsersWaitingResponse.objects.create(user=instance)