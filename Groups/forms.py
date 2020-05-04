from django import forms
from django.forms import ModelForm
from .models import MyGroup

class GroupForm(ModelForm):
    groupName = forms.CharField(max_length=100)
    purpose = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = MyGroup
        fields = ['purpose', 'groupName']
