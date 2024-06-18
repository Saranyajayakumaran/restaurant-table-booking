from django import forms
from django.forms import ModelForm
from .models import BookingTable


class BookingTableForm(forms.ModelForm):

    class Meta:
        model=BookingTable
        exclude=['user'] # excluding the user field, django automatically generate user id

