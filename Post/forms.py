from django import forms
from django.core.exceptions import ObjectDoesNotExist

from .models import Post, TabooUser
from .taboo import words
from Users.models import AcceptedUser
from Groups.models import GroupMember

class PostForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('request')
        super(PostForm, self).__init__(*args,**kwargs)
        self.fields['group'].queryset = GroupMember.objects.filter(member=self.user)

    group = forms.ModelChoiceField(queryset=None)
    title = forms.CharField(max_length=50)
    desc = forms.CharField(max_length=200, widget=forms.Textarea)

    class Meta:
        fields = [
            'group',
            'title',
            'desc'
        ]

    def save(self):
        data = self.cleaned_data   
        checkedString = ""
        tabooWord = False
        tabooWordUsed = None

        for word in data['desc'].split():
            if word in words:
                checkedString += "*** "
                tabooWord = True
                tabooWordUsed = word
            else:
                checkedString += (word + " ")

        Post.objects.create(group=data['group'].group, title=data['title'], desc=checkedString, user=self.user)

        if(tabooWord):
            try:
                TabooUser.objects.get(user=self.user, word=tabooWordUsed)
                user = AcceptedUser.objects.get(user=self.user)
                user.updateRep(-5)
                user.save()
            except ObjectDoesNotExist:
                TabooUser.objects.create(user=self.user, word=tabooWordUsed)
                user = AcceptedUser.objects.get(user=self.user)
                user.updateRep(-1)
                user.save()

    def getGroup(self):
        data = self.cleaned_data
        return  data['group'].group