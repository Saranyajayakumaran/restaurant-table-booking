"""
Imports
"""
import datetime
from datetime import date,datetime,time,timedelta
import pytz
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import TableBooking

class CustomerSignUpForm(UserCreationForm):
    """
    Form to register new user
    """
    username= forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'letters, digits, @/./+/-/_'}),
        help_text="*"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter same password'}),
        help_text="*"
    )


    class Meta:
        """
        Get all the required fileds from usercreationForm
        """
        model = User
        fields = ('first_name','last_name','email','username','password1','password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        if len(password1) < 8:  # Custom password length validation
            raise ValidationError("Password is too short, it must be at least 8 characters long")
        return password2

    def clean_email(self):
        """
        Validate the emaila adress it should contain @
        """
        email=self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Email is required")
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with the email already exist, Please give another email id")
        return email

    def clean_username(self):
        username=self.cleaned_data.get("username")
        if not username:
            raise ValidationError("Username field cannot be empty")
        if len(username)<8:
            raise ValidationError("Username should contain atleast 8 characters")
      
        allowed_characters = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.@+-_')
        if not all(char in allowed_characters for char in username):
            raise ValidationError("Username can only contain letters, digits, and @/./+/-/_ characters")
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists")
        return username

    def clean_first_name(self):
        """
        Validate the firt name cannot be empty and digits
        """
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise ValidationError("First name field cannot be empty")
        if not first_name.isalpha():
            raise ValidationError("First name can only contain letters")
        return first_name

    def clean_last_name(self):
        """
        Validate last name cannot be empty and digits
        """
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise ValidationError("Last name field cannot be empty")
   
        if not last_name.isalpha():
            raise ValidationError("Last name can only contain letters")
        return last_name


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
            'table': forms.Select(attrs={'class': 'form-control small-input'}),
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control small-input'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control small-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control small-input'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control small-input'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control small-input', 'rows': 3, 'placeholder':''}),
        }
    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.pop('is_update', False)
        super().__init__(*args, **kwargs)

    def clean_booking_date(self):
        """
        Validate Past date cannot be booked and limit the booking depends on opening days
        """
        cleaned_data = self.cleaned_data
        user_selected_booking_date = cleaned_data.get('booking_date')
        user_selected_booking_time = cleaned_data.get('booking_time')
        table_data = cleaned_data.get('table')

        if user_selected_booking_date and user_selected_booking_time and table_data:
            booking_datetime = datetime.combine(user_selected_booking_date, user_selected_booking_time)
            if not self.is_update:  # ensure it is not update 
                booking_exists = TableBooking.objects.filter(
                    table=table_data,
                    booking_date=user_selected_booking_date,
                    booking_time=user_selected_booking_time
                ).exists()
            
            if booking_exists:
                raise ValidationError(f"The table {table_data} is already booked at {booking_datetime}. Please select another time.")

        if user_selected_booking_date<date.today():
            raise ValidationError("Please select another date in future, you cannot book a table in past date")
        
        if user_selected_booking_date.weekday()==1:
            raise ValidationError("Restaurant is closed on Tuesdays,please select another date")
        return user_selected_booking_date
    
    def clean_booking_time(self):
        """
        Validate past time cannot be booked
        """

        cet = pytz.timezone('CET')#Central european time

        user_selected_booking_date = self.cleaned_data.get('booking_date')
        user_selected_booking_time = self.cleaned_data.get('booking_time')

        if user_selected_booking_date and user_selected_booking_time:
            # Combine date and time and localize to CET timezone
            booking_datetime_naive = datetime.combine(user_selected_booking_date, user_selected_booking_time)
            booking_datetime_cet = cet.localize(booking_datetime_naive)
            
            #current time in CET timezone
            current_time_cet = datetime.now(pytz.utc).astimezone(cet)
            
            # Validate booking is in the future
            if booking_datetime_cet < current_time_cet:
                raise ValidationError("Please select a future time, Booking date cannot be in the past.")

            # Define restaurant operating hours in CET
            restaurant_opening_time = time(11, 0)
            restaurant_closing_time = time(23, 0)

            if not (restaurant_opening_time <= user_selected_booking_time <= restaurant_closing_time):
                # Table can be booked only during operating hours
                raise ValidationError("Please select time within (11:00 AM to 9:00 PM) CET")
            
            # Validate booking is at least 2 hours before closing
            closing_datetime_naive = datetime.combine(user_selected_booking_date, restaurant_closing_time)
            closing_datetime_cet = cet.localize(closing_datetime_naive)

            if booking_datetime_cet > closing_datetime_cet - timedelta(hours=2):
                raise ValidationError("Please select time within (11:00 AM to 9:00 PM) CET")

        return user_selected_booking_time

    
    def clean_phone_number(self):
        """
        Validate phone number field to ensure the phone numbers are digits
        """
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            if not phone_number.isdigit():
                raise ValidationError("Phone number can only contain digits. Please enter a valid number.")
            # Convert phone_number to string to count digits
            phone_number = str(phone_number)
            if len(phone_number)<10:
                raise ValidationError("Phone number cannot be less than 10 digits,please enter a valid number")
        return phone_number
    
    def clean_number_of_guests(self):
        """
        Validate number of guests, cannot be 0
        """
        number_of_guests = self.cleaned_data.get('number_of_guests')
        if number_of_guests <= 0:
            raise ValidationError("Number of guests must be greater than zero.")
        return number_of_guests

    def clean_special_requests(self):
        """
        Validate special request field cannot be more than 200 characters
        """
        special_requests = self.cleaned_data.get('special_requests')
        if special_requests and len(special_requests) > 200:
            raise ValidationError("Special requests must be less than 200 characters.")
        return special_requests

    def clean(self):
        cleaned_data = super().clean()
        self.validate_table_capacity(cleaned_data)
        self.validate_update()
        return cleaned_data

    def validate_table_capacity(self,cleaned_data):
        """
        Validate table capacity and number of guests
        if no.of.guests esceed table capacity 
        """
        
        table_data=cleaned_data.get('table')
        number_of_guests=cleaned_data.get('number_of_guests')

        if table_data and number_of_guests:
            if number_of_guests>table_data.seats:
                self.add_error('number_of_guests', f"The selected table can only accommodate {table_data.seats} persons. Please select another table.")

        return table_data
    
    def validate_update(self):
        """
        Validate update form, Chack for current instance, 
        if it is cuttent instance skip and validate other datas 
        """
        cleaned_data = self.cleaned_data
        table_data = cleaned_data.get('table')
        user_selected_booking_date = cleaned_data.get('booking_date')
        user_selected_booking_time = cleaned_data.get('booking_time')

        # Skip conflict booking validation during update
        # Check if user_selected_booking_date and user_selected_booking_time are provided
        if user_selected_booking_date and user_selected_booking_time:
                # Combine date and time
            booking_datetime = datetime.combine(user_selected_booking_date, user_selected_booking_time)
            current_id = self.instance.id if self.instance else None

            print(f"Debug - Current instance ID: {current_id}")
            print(f"Debug - Booking datetime: {booking_datetime}")

            # Check for existing bookings at the same date and time
            booking_exists= TableBooking.objects.filter(
                table=table_data,
                booking_date=user_selected_booking_date,
                booking_time=user_selected_booking_time
            )
            if current_id:
                booking_exists = booking_exists.exclude(id=current_id)
                print(f"excluded id:{current_id}")
            
            print(f"Debug - Query: {booking_exists.query}")

            if booking_exists.exists():
                self.add_error('booking_date', f"The table {table_data} is already booked at {booking_datetime}. Please select another time")