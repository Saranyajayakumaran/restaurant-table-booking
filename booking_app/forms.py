from django import forms
from django.forms import ModelForm
from .models import BookingTable
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import SignupModel



class BookingTableForm(forms.ModelForm):

    class Meta:
        model=BookingTable
        exclude=['user'] # excluding the user field, django automatically generate user id


class CustomerSignUpForm(UserCreationForm):
    email=forms.EmailField(max_length=254,help_text='required')
    phone_number=forms.CharField(max_length=20,required=True)
    class Meta:
        model = SignupModel
        fields = ('username','name','email', 'phone_number')  