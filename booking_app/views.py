"""
Required imports
"""
from datetime import date
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, logout,login
from django.contrib.auth.decorators import login_required
from .models import HomePageContent, MenuPageContent, TableBooking
from .forms import CustomerSignUpForm, CustomerLoginForm, TableBookingForm

#from .models import SignupModel


# Create your views here.
def homepage(request):
    """
    Home page contect
    """
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
        signup_form = CustomerSignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            #return redirect('login')
    else:
        signup_form = CustomerSignUpForm()
    return render(request, 'signup.html', {'signup_form': signup_form})


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
                    #print("entering login page")
                    return redirect('booking')
                else:
                    error_message = "Account is disabled"
            else:
                error_message = "Invalid username or password"
          
            form.fields['password'].widget.attrs['value'] = ''

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

@login_required
def table_booking_view(request):
    """
    booking table allow user to book a table in restaurant 
    if form is valid it save all the data in database
    """
    print("i am in booking page")
    #delete_user_old_bookings(request)

    #print("i am in booking page")
    if request.method == 'POST':
        booking_form = TableBookingForm(request.POST)
        if booking_form.is_valid():
            booking=booking_form.save(commit=False)
            booking.user=request.user
            print("Form cleaned data:", booking_form.cleaned_data)  # Check form's cleaned data
            print("Phone number before saving:", booking.phone_number)
            booking.save()
            print("Saved booking data:")
            print(f"Table: {booking.table}")
            print(f"Booking Date: {booking.booking_date}")
            print(f"Booking Time: {booking.booking_time}")
            print(f"Phone Number: {booking.phone_number}")
            print(f"Number of Guests: {booking.number_of_guests}")
            print(f"Special Requests: {booking.special_requests}")
            messages.success(request, "Booking successfull.Thank you for booking with us!")
            booking_form = TableBookingForm()
    else:
        booking_form = TableBookingForm()

    #print("Rendering form")  #
    return render(request, 'booking.html', {'booking_form': booking_form})

def delete_user_old_bookings(request):
    """
    Delete old bookings for logged in user
    """
    all_bookings = TableBooking.objects.all().filter(user=request.user)
    deleted_bookings=[]
    for booking in all_bookings:
        if booking.booking_date < date.today():
            booking.delete()
            deleted_bookings.append(booking)
    return deleted_bookings

@login_required
def user_booking_list(request):
    """
    List all bookings made by the logged-in user.
    """
    all_bookings = TableBooking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': all_bookings})

@login_required
def user_booking_update(request,booking_id):
    """
    Update an existing booking.
    """
    print("inside update")
    booking = get_object_or_404(TableBooking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        form = TableBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully")
            return redirect("user_booking_list") #redirect to same page
        else:
            print("Form errors:", form.errors)
    else:
        form = TableBookingForm(instance=booking)
    return render(request, "booking_update.html", {'form': form})

@login_required
def user_booking_delete(request,booking_id):
    """
    Delete the selected existing  booking.
    """
    print("Debug: user_booking_delete()")
    booking = get_object_or_404(TableBooking, id=booking_id, user=request.user)
    if request.method == 'GET':
        print("it is a GET")
        booking.delete()
        print("record deleted")
        messages.success(request, "Booking deleted successfully.")
    return redirect('user_booking_list')

    #return render(request, 'delete.html', {'booking': booking})

def booking_confirm_delete(request, booking_id):
    booking = get_object_or_404(TableBooking, id=booking_id)
    return render(request, 'delete.html', {'booking': booking})
