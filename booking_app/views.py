from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import HomePageContent
from .models import MenuPageContent
from .models import TableInfo

#from .models import BookingTable
#from .forms import BookingTableForm
from .forms import CustomerSignUpForm
from .forms import CustomerLoginForm
import datetime
from datetime import timedelta

#from .models import SignupModel


# Create your views here.
def homepage(request):
    content=HomePageContent.objects.first()
    #contact_details=ContactInformation.objects.first()
    return render(request,'home.html',{'content':content})

def menupage(request):
    """
    view to store and diaplay all the menu items in webpage
    """
    menu_items=MenuPageContent.objects.all()
    return render(request,'menu.html',{'menu_items':menu_items})

def signup_view(request):
    """
    sign up view checks weather all fields in form filled and save the data in database
    """
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = CustomerSignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """
    view for login functionality
    authenticate before login, check for correct username and password 
    do action based on authentication
    """
    if request.method=="POST":
        form=CustomerLoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    print("entering login page")
                    return HttpResponse("booking page")
                else:
                    error_message = "Account is disabled"
            else:
                error_message = "Invalid username or password"

            return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form=CustomerLoginForm()
    return render(request,'login.html',{"form":form})


@login_required
def logout_view(request):
    """
    Logout view allow user to logout and render home page
    """
    logout(request)
    return render(request,'home.html')

def table_info_list(request):
    tables = TableInfo.objects.all()
    return render(request, 'table_info_list.html', {'tables': tables})