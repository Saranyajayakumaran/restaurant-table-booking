from django import forms
from django.forms import ModelForm
from .models import BookingTable
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class BookingTableForm(forms.ModelForm):

    class Meta:
        model=BookingTable
        exclude=['user'] # excluding the user field, django automatically generate user id

class UserRegistrationForm(UserCreationForm):
    
    class Meta:
        model=User
        fields={ 'first_name',
                'last_name',
                'email',
                'username'}
