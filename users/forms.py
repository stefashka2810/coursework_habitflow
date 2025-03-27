from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User

class UserRegisterForm(UserCreationForm):
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Your password must contain at least 8 characters"
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Enter the same password as before, for verification"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'gender', 'email', 'password1', 'password2']
        
    def clean_password2(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User