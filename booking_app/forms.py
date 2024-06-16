from django import forms
from django.forms import ModelForm
from .models import BookingTable

class BookingTableForm(forms.ModelForm):

    class Meta:
        model=BookingTable
        fields='__all__'
