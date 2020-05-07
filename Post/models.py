from django.db import models
from django.contrib.auth.models import User

from Groups.models import Group

class Post(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    desc = models.TextField(max_length=200, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title