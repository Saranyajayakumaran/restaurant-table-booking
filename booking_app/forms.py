from django import forms
from django.forms import ModelForm
from .models import BookingTable
from .models import Registration

class BookingTableForm(forms.ModelForm):

    class Meta:
        model=BookingTable
        exclude=['user'] # excluding the user field, django automatically generate user id

class RegistrationForm(forms.ModelForm):
    
    class Meta:
        model=Registration
        fields='__all__'
