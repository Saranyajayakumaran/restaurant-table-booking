import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import SignUpModel



class CustomerSignUpForm(UserCreationForm):
    """
    Form to register new user
    """
    phone_number = forms.CharField(max_length=15, help_text='Enter your phone number')
    class Meta:
        """
        Get all the required fileds from usercreationForm
        """
        model = User
        fields = ('username','email','first_name','last_name','phone_number','password1','password2') 

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        
        if len(password1) < 8:  # Custom password length validation
            raise ValidationError("Password is too short, it must be at least 8 characters long")
        
        return password2
    
class CustomerLoginForm(forms.Form):
    """
    Form for user authentication , allow user to login
    """
    username=forms.CharField(max_length=200)
    password=forms.CharField(widget=forms.PasswordInput)

