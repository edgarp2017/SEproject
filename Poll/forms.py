from django.forms import ModelForm
from.models import Poll

class CreatePollForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        self.user = kwargs.pop('request')
        super(CreatePollForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Poll
        fields = ['question', 'ans_one', 'ans_two', 'ans_three']


    def checkVoted(self):
        data = self.cleaned_data
        poll = Polls.objects.get(pk=group.pk)
        voters = poll.Voter.all()
        for vote in voters:
            if vote.username == self.user.username:
                return True
        return False
