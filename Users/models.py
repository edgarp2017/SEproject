from django.db import models
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
        