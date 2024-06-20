from django import forms
from django.forms import ModelForm
from .models import BookingTable
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
#from .models import SignupModel



class BookingTableForm(forms.ModelForm):

    class Meta:
        model=BookingTable
        exclude=['user'] # excluding the user field, django automatically generate user id


class CustomerSignUpForm(UserCreationForm):
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
    username=forms.CharField(max_length=200)
    password=forms.CharField(widget=forms.PasswordInput)