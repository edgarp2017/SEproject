from django import forms
from Users.models import AcceptedUser

class InitialReputationForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('request')
        super(InitialReputationForm, self).__init__(*args,**kwargs)
        self.fields['users'].queryset = AcceptedUser.objects.filter(reference=self.user)

    users = forms.ModelChoiceField(queryset=None)
    score = forms.IntegerField()
    
    class Meta:
        fields = [
            'users',
            'score'
        ]

    def save(self, role):
        data = self.cleaned_data
        user = data['users']

        if role == 'OU':
            if ((data['score'] >= 0) and (data['score'] <= 10)):     
                user.updateRep(data['score'])
                user.updateReference()
                user.save()
                return True
        else:
            if ((data['score'] >= 0) and (data['score'] <= 20)):     
                user.updateRep(data['score'])
                user.updateReference()
                user.save()
                return True
                
        return False