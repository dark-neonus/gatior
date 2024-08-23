# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class RegisterForm(UserCreationForm):
    """
    Form to register an Account with additional fields.
    """
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]

    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        user.password = self.cleaned_data["password1"]
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=Account._meta.get_field("username").max_length)
    password = forms.CharField(widget=forms.PasswordInput)