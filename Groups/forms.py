from django import forms
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist

from .models import Group, InviteUser, Post, GroupMember
from Users.models import AcceptedUser
from .taboo import words

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['groupName',
            'purpose']

    def checkExist(self):
        data = self.cleaned_data
        try:
            Group.objects.get(groupName=data['groupName'])
        except ObjectDoesNotExist:
            return False
        return True


class GroupInviteForm(ModelForm):
    class Meta:
        model = InviteUser
        fields = [
            'sent_to',
        ]

class PostForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('request')
        super(PostForm, self).__init__(*args,**kwargs)
        self.fields['group'].queryset = GroupMember.objects.filter(member=self.user)

    group = forms.ModelChoiceField(queryset=None)
    title = forms.CharField(max_length=50)
    desc = forms.CharField(max_length=200, widget=forms.Textarea)

    class Meta:
        model = Post
        widgets = { 'desc': forms.TextInput(attrs={'size': 80})}
        fields = [
            'group',
            'title',
            'desc'
        ]

    def save(self):
        data = self.cleaned_data   
        checkedString = ""
        tabooWord = False

        for word in data['desc'].split():
            if word in words:
                checkedString += "*** "
                tabooWord = True
            else:
                checkedString += (word + " ")

        Post.objects.create(group=data['group'].group, title=data['title'], desc=checkedString)

        if(tabooWord):
            user = AcceptedUser.objects.get(user=self.user)
            user.updateRep(-1)
            user.save()