from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from gpa_webservice.models import User


class SignUpForm(UserCreationForm):
    """ Signup form """
    # first_name = forms.CharField(required=True)
    # last_name = forms.CharField(required=True)
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'department']

