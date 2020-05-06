from django.db import models

class Poll(models.Model):

    question = models.TextField()

    ans_one = models.CharField(max_length=30)
    ans_two = models.CharField(max_length=30)
    ans_three = models.CharField(max_length=30)

    ans_one_votes = models.IntegerField(default=0)
    ans_two_votes = models.IntegerField(default=0)
    ans_three_votes = models.IntegerField(default=0)

    def total(self):
        return self.ans_one_votes + self.ans_two_votes + self.ans_three_votes


