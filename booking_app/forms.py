from django.forms import ModelForm
from .models import BookingTable

class BooingTable_Form(forms.ModelForm):

    class Meta:
        model=BookingTable
        fields='__all__'