"""
Imports
"""
import datetime
from datetime import date, datetime, time, timedelta
import pytz
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import TableBooking


class CustomerSignUpForm(UserCreationForm):
    """
    Form to register a new user
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':
                                      'letters, digits, @,.,+,-,_'}),
        help_text="*"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':
                                          'Enter same password'}),
        help_text="*"
    )

    class Meta:
        """
        Get all the required fields from UserCreationForm
        """
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password1', 'password2')

    def validate_passwords(self):
        """
        Validate passwords for not same and too short
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                self.add_error('password2', "Passwords don't match")
            if len(password1) < 8:
                self.add_error('password1', "Password is too short,"
                               " it must be at least 8 characters long")

    def validate_email(self):
        """
        Validate email id for alrady available in database
        """
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', "A user with this email already exists."
                           "Please use another email address")

    def validate_username(self):
        """
        Validate username for allowed characters,
        alrady available in database,
        atleast 8 char length
        """

        username = self.cleaned_data.get("username")
        if username:
            if len(username) < 8:
                self.add_error('username',
                               "Username should contain at least 8 characters")
            else:
                allowed_characters = set('abcdefghijklmnopqrstuvwxyz'
                                         'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                                         '0123456789.@+-_')
                if not all(char in allowed_characters for char in username):
                    self.add_error('username',
                                   "Username can only contain letters,"
                                   "digits, and @,.,+,-,_ characters")
                elif User.objects.filter(username=username).exists():
                    self.add_error('username', "Username already exists,"
                                   "Please give another username")

    def validate_first_name(self):
        """
        Validate first name for only letters
        """
        first_name = self.cleaned_data.get("first_name")
        if first_name and not first_name.isalpha():
            self.add_error('first_name', "First name can only contain letters")

    def validate_last_name(self):
        """
        Validate last name for only letters
        """
        last_name = self.cleaned_data.get("last_name")
        if last_name and not last_name.isalpha():
            self.add_error('last_name', "Last name can only contain letters")

    def clean(self):
        """
        Call all the validation functions for each field.
        """
        cleaned_data = super().clean()

        self.validate_first_name()
        self.validate_last_name()
        self.validate_email()
        self.validate_username()
        self.validate_passwords()

        return cleaned_data


class CustomerLoginForm(forms.Form):
    """
    Form for user authentication , allow user to login
    """
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)


class TableBookingForm(forms.ModelForm):
    """
    Get all the fields from tablebooking model
    """
    class Meta:
        """
        Get the fields of table booking form
        """
        model = TableBooking
        fields = ['table',
                  'booking_date',
                  'booking_time',
                  'phone_number',
                  'number_of_guests',
                  'special_requests']
        widgets = {
            'table': forms.Select(attrs={'class': 'form-control small-input'}),
            'booking_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control small-input'}),
            'booking_time': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control small-input'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control small-input'}),
            'number_of_guests': forms.NumberInput(attrs={'class':
                                                  'form-control small-input'}),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control small-input',
                'rows': 3, 'placeholder': ''}),
        }

    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.pop('is_update', False)
        super().__init__(*args, **kwargs)

    def clean_booking_date(self):
        """
        Validate Past date cannot be booked
        and limit the booking depends on
        opening days
        """
        cleaned_data = self.cleaned_data
        user_selected_booking_date = cleaned_data.get('booking_date')
        user_selected_booking_time = cleaned_data.get('booking_time')
        table_data = cleaned_data.get('table')

        if (user_selected_booking_date and
                user_selected_booking_time and
                table_data):

            booking_datetime = (
                datetime.combine(user_selected_booking_date,
                                 user_selected_booking_time)
                )
            if not self.is_update:  # ensure it is not update
                booking_exists = TableBooking.objects.filter(
                    table=table_data,
                    booking_date=user_selected_booking_date,
                    booking_time=user_selected_booking_time
                ).exists()

            if booking_exists:
                raise ValidationError(
                    f"The table {table_data} is already booked at"
                    f"{booking_datetime}"
                    "Please select another time.")

        if user_selected_booking_date < date.today():
            raise ValidationError(
                "Please select another date in future,"
                "you cannot book a table in past date")

        if user_selected_booking_date.weekday() == 1:
            raise ValidationError("Restaurant is closed on Tuesdays,"
                                  "Please select another date")
        return user_selected_booking_date

    def clean_booking_time(self):
        """
        Validate past time cannot be booked
        """
        user_selected_booking_date = self.cleaned_data.get('booking_date')
        user_selected_booking_time = self.cleaned_data.get('booking_time')
        # Combine date and time and covert to utc timezone
        if user_selected_booking_date and user_selected_booking_time:

            booking_datetime_basic = datetime.combine(
                user_selected_booking_date, user_selected_booking_time)
            # convert user selected booking datetime to utc
            booking_datetime_utc = pytz.utc.localize(booking_datetime_basic)

            # get current time and convert current time to utc
            current_time_utc = datetime.now(pytz.utc)

            # Validate bookingtime in the future
            if booking_datetime_utc < current_time_utc:
                raise ValidationError(
                    "Please select a future time")

            # Defining restaurant operating hours in UTC
            restaurant_opening_time_utc = time(10, 0)  # 11.00am CET
            restaurant_closing_time_utc = time(22, 0)  # 23.00 CET

            if not (restaurant_opening_time_utc
                    <= user_selected_booking_time <=
                    restaurant_closing_time_utc):
                # Table can be booked only during operating hours
                raise ValidationError("Please select time within"
                                      "(10:00 AM to 10:00 PM) UTC")

            # Validate booking is at 2 hours before closing
            closing_datetime_basic = datetime.combine(
                user_selected_booking_date, restaurant_closing_time_utc)
            closing_datetime_utc = pytz.utc.localize(closing_datetime_basic)

            if (
                booking_datetime_utc >
                closing_datetime_utc - timedelta(hours=2)
            ):
                raise ValidationError("Please select time within"
                                      "(10:00 AM to 8:00 PM) UTC")

        return user_selected_booking_time

    def clean_phone_number(self):
        """
        Validate phone number field to ensure the phone numbers are digits
        """
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            if not phone_number.isdigit():
                raise ValidationError("Phone number can only contain digits."
                                      "Please enter a valid number.")
            # Convert phone_number to string to count digits
            phone_number = str(phone_number)
            if len(phone_number) < 10:
                raise ValidationError("Phone number cannot be"
                                      "less than 10 digits,"
                                      "Please enter a valid number")
        return phone_number

    def clean_number_of_guests(self):
        """
        Validate number of guests, cannot be 0
        """
        number_of_guests = self.cleaned_data.get('number_of_guests')
        if number_of_guests <= 0:
            raise ValidationError("Number of guests must"
                                  "be greater than zero.")
        return number_of_guests

    def clean_special_requests(self):
        """
        Validate special request field cannot be more than 200 characters
        """
        special_requests = self.cleaned_data.get('special_requests')
        if special_requests and len(special_requests) > 200:
            raise ValidationError("Special requests must be"
                                  "less than 200 characters.")
        return special_requests

    def clean(self):
        cleaned_data = super().clean()
        self.validate_table_capacity(cleaned_data)
        self.validate_update()
        return cleaned_data

    def validate_table_capacity(self, cleaned_data):
        """
        Validate table capacity and number of guests
        if no.of.guests esceed table capacity
        """
        table_data = cleaned_data.get('table')
        number_of_guests = cleaned_data.get('number_of_guests')

        if table_data and number_of_guests:
            if number_of_guests > table_data.seats:
                self.add_error(
                    'number_of_guests',
                    (
                        f"The selected table can only"
                        f"accommodate {table_data.seats} "
                        "persons. Please select another table."
                    )
                )
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

        # Check user_selected_booking_date and
        # user_selected_booking_time are provided
        if user_selected_booking_date and user_selected_booking_time:
            # Combine date and time
            booking_datetime = datetime.combine(
                user_selected_booking_date, user_selected_booking_time)
            current_id = self.instance.id if self.instance else None

            # Check for existing bookings at the same date and time
            booking_exists = TableBooking.objects.filter(
                table=table_data,
                booking_date=user_selected_booking_date,
                booking_time=user_selected_booking_time
            )
            if current_id:
                booking_exists = booking_exists.exclude(id=current_id)

            if booking_exists.exists():
                self.add_error('booking_date',
                               f"The table {table_data} is already booked"
                               f" at {booking_datetime}."
                               "Please select another time")
