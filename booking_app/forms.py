"""
Imports
"""
import datetime
from datetime import date,datetime,time
from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import TableBooking



class CustomerSignUpForm(UserCreationForm):
    """
    Form to register new user
    """
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
        Validate Past date cannot be booked and limit the booking depends on opening days
        """
        user_selected_booking_date=self.cleaned_data.get('booking_date')
        if user_selected_booking_date<date.today():
            raise ValidationError("Please select another date in future, you cannot book a table in past date")
        
        if user_selected_booking_date.weekday()==1:
            raise ValidationError("Restaurant is closed on Tuesdays,please select another date")
        return user_selected_booking_date
    
    
    def clean_booking_time(self):
        """
        Validate past time cannot be booked
        """
        user_selected_booking_date = self.cleaned_data.get('booking_date')
        user_selected_booking_time = self.cleaned_data.get('booking_time')
        
        if user_selected_booking_date and user_selected_booking_time:
            booking_datetime = datetime.combine(user_selected_booking_date, user_selected_booking_time)
            if booking_datetime < datetime.now():
                raise ValidationError("Please select a future time, you cannot book a table in the past.")
            
        restaurant_opening_time=time(11,0)
        restaurant_closing_time=time(21,0)

        if not (restaurant_opening_time<=user_selected_booking_time<=restaurant_closing_time):
            # Table can be booked only 2hours before closing time
            raise ValidationError("Please select time within (11.00 AM to 21.00 PM)")
        return user_selected_booking_time
    

    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.pop('is_update', False)  # Custom flag to indicate update
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if not self.is_update:
            self.validate_update()

        return cleaned_data

    def validate_update(self):
        cleaned_data = self.cleaned_data
        table_data = cleaned_data.get('table')
        number_of_guests = cleaned_data.get('number_of_guests')
        user_selected_booking_date = cleaned_data.get('booking_date')
        user_selected_booking_time = cleaned_data.get('booking_time')

        # Validate table seats only if number_of_guests and table_data are provided
        if table_data and number_of_guests:
            if number_of_guests > table_data.seats:
                raise ValidationError(f"The selected table can only accommodate {table_data.seats} persons. Please select another table.")
                
        # Skip conflict booking validation during update
        # Check if user_selected_booking_date and user_selected_booking_time are provided
        if user_selected_booking_date and user_selected_booking_time:
            if not self.instance.id:  # Ensure this is a new instance (create operation)
                # Combine date and time
                booking_datetime = datetime.combine(user_selected_booking_date, user_selected_booking_time)

                # Check for existing bookings at the same date and time
                booking_exists= TableBooking.objects.filter(
                    table=table_data,
                    booking_date=user_selected_booking_date,
                    booking_time=user_selected_booking_time
                ).exists()

                if booking_exists:
                    raise ValidationError(f"The table {table_data} is already booked at {booking_datetime}. Please select another time.")