from django import forms
from django.core.exceptions import ObjectDoesNotExist

from .models import Post
from Users.models import AcceptedUser

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'desc'
        ]
