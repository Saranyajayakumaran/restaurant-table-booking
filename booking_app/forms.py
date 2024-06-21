from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import BookingTable


class CustomerSignUpForm(UserCreationForm):
    """
    Form to register new user
    """
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')  

    #def clean_password2(self):
        #password1 = self.cleaned_data.get("password1")
        #password2 = self.cleaned_data.get("password2")
        
        #if password1 and password2 and password1 != password2:
            #raise ValidationError("Passwords don't match")
        
        #if len(password1) < 8:  # Custom password length validation
            #raise ValidationError("Password is too short, it must be at least 8 characters long")
        
        #return password2

class CustomerLoginForm(forms.Form):
    """
    Form for user authentication , allow user to login
    """
    username=forms.CharField(max_length=200)
    password=forms.CharField(widget=forms.PasswordInput)

class BookingTableForm(forms.ModelForm):
    """
    Form to book a table in the restaurant
    """
    class Meta:
        model=BookingTable
        fields=('date','time','number_of_guests','special_requests','table')
