from django import forms
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    firstName = forms.CharField()
    lastName = forms.CharField()
    email = forms.EmailField()
    interest = forms.CharField()
    credential = forms.CharField()
    reference = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'firstName',
            'lastName',
            'email',
            'interest',
            'credential',
            'reference',
        ]

class NewUserForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit'))
    user = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxInput,
        choices = User.objects.all().filter(is_active=False),
    )
    answer = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices = [
            ('accept', 'Accept'),
            ('reject', 'Reject')
        ],
    )

    class Meta:
        model = User
        fields = [
            'user',
            'answer'
        ]