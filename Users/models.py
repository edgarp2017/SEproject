from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Application(models.Model):
    email = models.EmailField(max_length=254, null=False)
    firstName = models.CharField(max_length=50, null=False)
    lastName = models.CharField(max_length=50, null=False)
    interest = models.CharField(max_length=100, null=False)
    credential = models.CharField(max_length=100, null=False)
    reference = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.firstName+ ' ' + self.lastName

    def getEmail(self):
        return self.email

    def getfirstName(self):
        return self.firstName

    def getlastName(self):
        return self.lastName

    def getReference(self):
        return self.reference

class AcceptedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_OU = models.BooleanField(default=True)
    is_VIP = models.BooleanField(default=False)
    is_SU = models.BooleanField(default=False)
    rep_score = models.IntegerField(default=0)
    reference = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user.username

    def updateRep(self, amount):
        self.rep_score += amount

        if self.is_OU:
            print(self.rep_score)
            if self.rep_score > 30:
                self.is_OU = False
                self.is_VIP = True
            
            if self.rep_score < 0:
                BlackList.objects.create(email=self.user.email)
                self.user.delete()
                
        if self.is_VIP:
            if self.rep_score < 20:
                self.is_VIP = False
                self.is_OU = True
    
    def updateReference(self):
        self.reference = None

    def getRole(self):
        if self.is_OU:
            return "OU"
        elif self.is_VIP:
            return "VIP"
        else:
            return "SU"
            
class BlackList(models.Model):
    email = models.EmailField(max_length=254, null=False)
    
    def __str__(self):
        return self.email

class RejectedUser(models.Model):
    email = models.EmailField(max_length=254, null=False)
    
    def __str__(self):
        return self.email

class WhiteBox(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='WhiteBoxuser')
    whitebox = models.ManyToManyField(User, related_name='whitebox')

    def __str__(self):
        return "%s WhiteBox" %self.user

class BlackBox(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='BlackBoxuser')
    blackbox = models.ManyToManyField(User, related_name='blackbox', default="You are in my black box.")
    message = models.CharField(max_length=100)

    def __str__(self):
        return "%s BlackBox" %self.user
        
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        WhiteBox.objects.create(user=instance)
        BlackBox.objects.create(user=instance)