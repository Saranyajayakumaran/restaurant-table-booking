from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import BookingTable
import datetime


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

class BookingTableForm(forms.ModelForm):
    """
    Form to book a table in the restaurant
    """
    class Meta:
        model=BookingTable
        fields=('date','time','number_of_guests','special_requests','table')
        widgets={
            'date':forms.DateInput(attrs={'type':'date'}),
            'time':forms.TimeInput(attrs={'type':'time'})
        }

    def time_of_booking(self):
        """
        Limit the time of booking only in opening hours
        """
        time=self.cleaned_data.get('time')
        morning_open_time_start=datetime.time(11,0)
        morning_open_time_end=datetime.time(14,0)
        evening_open_time_start=datetime.time(17,0)
        evening_open_time_end=datetime.time(23,0)

        if not(morning_open_time_start<= time <= morning_open_time_end or evening_open_time_start <=time <=evening_open_time_end):
            raise ValidationError("Please select booking time between 11am to 14.00pm and 17pm to 23pm")
        return time

    def date_of_booking(self):
        """
        Limit the date of booking depends on openeing days
        """
        date=self.cleaned_data.get('date')
        if date.weekday()==1:
            raise ValidationError("Restaurant is closed on tuesdays, Please select the another date")
        return date

