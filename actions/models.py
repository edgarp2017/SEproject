from django.db import models
from Users.models import AcceptedUser
from django.contrib.auth.models import User

# Create your models here.
class compliment(models.Model):
    user = models.ForeignKey(AcceptedUser, on_delete=models.CASCADE)
    praises = models.IntegerField(default=0)


    def __str__(self):
        return self.user

  
class complaint(models.Model):
    email = models.EmailField(max_length=254, null=False)
    firstName = models.CharField(max_length=50, null=False)
    lastName = models.CharField(max_length=50, null=False)
    guiltyUser = models.CharField(max_length=100, null=True)
    guiltyGroup = models.CharField(max_length=100, null=True)
    Reason = models.CharField(max_length=300, null=False)
    
