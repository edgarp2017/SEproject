from django.forms import ModelForm
from.models import Poll

class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'ans_one', 'ans_two', 'ans_three']
