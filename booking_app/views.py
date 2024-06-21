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
from .models import ContactInformation
from .models import MenuPageContent
from .models import BookingTable
from .forms import CustomerSignUpForm
from .forms import CustomerLoginForm,BookingTableForm
#from .models import SignupModel


# Create your views here.
def homepage(request):
    content=HomePageContent.objects.first()
    contact_details=ContactInformation.objects.first()
    return render(request,'home.html',{'content':content,'contact_details':contact_details})

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
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = CustomerSignUpForm()
    return render(request, 'signup.html', {'form': form})


#class CustomLoginView(LoginView):
    #template_name = 'login.html'
    #authentication_form = AuthenticationForm

#def loginpage(request):
    #return render(request, 'login.html')

## login

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
                    return render(request,'booking.html',{"form":form})
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
    logout(request)
    return render(request,'home.html')


def booking_table_view(request):
    if request.method == 'POST':
        #print(request.POST) 
        booking_form = BookingTableForm(request.POST)
        if booking_form.is_valid():
            #print("Form is valid") 
            # Process form data here if needed
            # For example: save to database
            booking_form.save()
            return HttpResponse("Booking successfull")  # Redirect to a success page or another view
    else:
        booking_form = BookingTableForm()

    #print("Rendering form")  #
    return render(request, 'booking.html', {'booking_form': booking_form})

