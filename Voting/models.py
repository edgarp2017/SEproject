from django.db import models

class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Yes'),
        (2, 'No'),
    )
    #user = models.ManyToManyField(User)
    user_vote = models.IntegerField(choices=VOTE_CHOICES)
    #group = models.OneToOneField(MyGroup, on_delete=models.CASCADE)
    #user_vote_on = models.OneToOneField(User, on_delete=models.CASCADE)