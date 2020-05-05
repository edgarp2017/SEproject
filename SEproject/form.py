from django import forms
from Users.models import AcceptedUser

class InitialReputation(forms.Form):
    user = forms.ModelChoiceField(queryset=AcceptedUser.objects.all().filter(init_rep=False))
    score = forms.IntegerField()
    
    class Meta:
        fields = [
            'user',
            'score'
        ]

    def save(self, role):
        data = self.cleaned_data
        user = data['user']
        if role == 'OU':
            if ((data['score'] >= 0) and (data['score'] <= 10)):     
                user.init_repGiven()
                user.updateRep(data['score'])
                user.save()
        else:
            if ((data['score'] >= 0) and (data['score'] <= 20)):     
                user.init_repGiven()
                user.updateRep(data['score'])
                user.save()