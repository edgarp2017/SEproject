from django import forms
from django.forms import ModelForm
from .models import MyGroup

class GroupForm(ModelForm):
    gorupName = forms.CharField(max_length=100)
    purpose = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = MyGroup
        fields = ['owner', 'purpose', 'groupName']
