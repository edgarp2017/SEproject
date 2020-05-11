from django.db import models
from Groups.models import Group

class Poll(models.Model):

    question = models.TextField()

    ans_one = models.CharField(max_length=30)
    ans_two = models.CharField(max_length=30)
    ans_three = models.CharField(max_length=30)

    ans_one_votes = models.IntegerField(default=0)
    ans_two_votes = models.IntegerField(default=0)
    ans_three_votes = models.IntegerField(default=0)

    Group = models.OneToOneField(Group, on_delete=models.CASCADE)


    def total(self):
        return self.ans_one_votes + self.ans_two_votes + self.ans_three_votes


