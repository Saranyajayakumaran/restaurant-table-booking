import datetime
from datetime import date,datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import TableBooking



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
        return user_selected_booking_time
    
    def clean(self):
        """
        Validate table seats and number of guests
        """
        cleaned_data=super().clean()
        table_data=cleaned_data.get('table')
        number_of_guests=cleaned_data.get('number_of_guests')
        user_selected_booking_date = cleaned_data.get('booking_date')
        user_selected_booking_time = cleaned_data.get('booking_time')
        if table_data and number_of_guests:
            if number_of_guests > table_data.seats:
                raise ValidationError(f"The selected table can only accomodate {table_data.seats} persons, Please select another table")
        print(cleaned_data)

        if table_data and user_selected_booking_date and user_selected_booking_time:
            # Combine date and time
            booking_datetime = datetime.combine(user_selected_booking_date, user_selected_booking_time)

            # Check for existing bookings at the same date and time
            conflicting_bookings = TableBooking.objects.filter(
                table=table_data,
                booking_date=user_selected_booking_date,
                booking_time=user_selected_booking_time
            ).exists()

            if conflicting_bookings:
                raise ValidationError(f"The table {table_data} is already booked at {booking_datetime}. Please select another time.")
        return cleaned_data

   