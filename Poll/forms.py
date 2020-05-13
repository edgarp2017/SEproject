from django.forms import ModelForm
from.models import Poll
from Groups.models import Group
from Post.models import Post

class CreatePollForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group',None)
        self.user = kwargs.pop('request',None)
        super(CreatePollForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Poll
        fields = ['question', 'ans_one', 'ans_two', 'ans_three']


    def delete(self):
        group = Group.objects.get(name=self.group)
        members = group.members.all().count()

        poll = Poll.objects.get(Group=self.group)

        if poll.total() == members:
            desc = "Results from poll: %s, has %d votes, %s, has %d and %s has %d votes."%(poll.ans_one, poll.ans_one_votes, poll.ans_two, poll.ans_two_votes, poll.ans_three, poll.ans_three_votes)
            Post.objects.create(group=self.group, title=poll.question, desc=desc, user=self.user)

        poll.delete()





