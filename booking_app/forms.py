import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import SignUpModel
from .models import TableBooking
from datetime import date,datetime,time



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
        fields = ('username','email','first_name','last_name','password1','password2') 

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

class TableBookingForm(forms.ModelForm):
    """
    Get all the fields from tablebooking model
    """
    class Meta:
        model = TableBooking
        fields = ['table', 'booking_date', 'booking_time', 'phone_number', 'number_of_guests', 'special_requests']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_booking_date(self):
        """
        Validate Past date cannot be booked
        """
        booking_date=self.cleaned_data.get('booking_date')
        if booking_date<date.today():
            raise ValidationError("Please select another date in future, you cannot book a table in past date")
        return booking_date
    
    
    def clean_booking_time(self):
        """
        Validate past time cannot be booked
        """
        booking_date = self.cleaned_data.get('booking_date')
        booking_time = self.cleaned_data.get('booking_time')
        
        if booking_date and booking_time:
            booking_datetime = datetime.combine(booking_date, booking_time)
            if booking_datetime < datetime.now():
                raise ValidationError("Please select a future time, you cannot book a table in the past.")    
        return booking_time
    
    def clean(self):
        """
        Validate table seats and number of guests
        """
        cleaned_data=super().clean()
        table=cleaned_data.get('table')
        number_of_guests=cleaned_data.get('number_of_guests')
        if table and number_of_guests:
            if number_of_guests > table.seats:
                raise ValidationError(f"The selected table can only accomodate {table.seats}, Please select another table")
        print(cleaned_data)