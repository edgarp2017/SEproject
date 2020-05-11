from django.forms import ModelForm
from.models import Poll

class CreatePollForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group',None)
        self.user = kwargs.pop('request',None)
        super(CreatePollForm, self).__init__(*args, **kwargs)
        print(self.user)

    class Meta:
        model = Poll
        fields = ['question', 'ans_one', 'ans_two', 'ans_three']


    def checkVoted(self):
        data = self.cleaned_data
        poll = Polls.objects.get(pk=group.pk)
