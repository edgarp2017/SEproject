from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .taboo import words
from Groups.models import Group
from Users.models import AcceptedUser

class Post(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    desc = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    def checkTaboo(self):
        checkedString = ""
        tabooWord = False
        tabooWordUsed = None

        for word in self.desc.split():
            if word in words:
                checkedString += "*** "
                tabooWord = True
                tabooWordUsed = word
            else:
                checkedString += (word + " ")

        self.desc = checkedString

        if(tabooWord):
            try:
                TabooUser.objects.get(user=self.user, word=tabooWordUsed)
                user = AcceptedUser.objects.get(user=self.user)
                user.updateRep(-5)
                user.save()
            except ObjectDoesNotExist:
                TabooUser.objects.create(user=self.user, word=tabooWordUsed)
                user = AcceptedUser.objects.get(user=self.user)
                user.updateRep(-1)
                user.save()

class TabooUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=50)

    def __str__(self):
        return "%s: %s" %(self.user, self.word)