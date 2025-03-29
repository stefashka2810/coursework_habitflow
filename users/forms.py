from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import User

class UserRegisterForm(UserCreationForm):
    
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
    # def clean_password2(self):

    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
        
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError("Passwords don't match")
    #     return password2
    


class UserLoginForm(AuthenticationForm):

    username = forms.CharField()

    password = forms.CharField()
    
    # error_messages = {
    #     'invalid_login': "Invalid email or password",
    #     'inactive': "This account is inactive.",
    # }

    class Meta:
        model = User
        fields = ['username', 'password']
