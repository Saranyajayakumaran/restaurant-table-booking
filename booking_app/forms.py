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
        fields={'username','email','last_name','first_name' }

        
        
    def save(self, commit=True):
        user=super(UserRegistrationForm,self).save(commit=False)
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']
        user.username=self.cleaned_data['username']
        if commit:
            user.save()
        return user