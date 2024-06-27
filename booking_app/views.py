from datetime import date
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
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
                    #print("entering login page")
                    return redirect('booking')
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

def table_booking_view(request):
    """
    booking table allow user to book a table in restaurant 
    if form is valid it save all the data in database
    """
    delete_user_old_bookings(request)

    #print("i am in booking page")
    if request.method == 'POST':
        booking_form = TableBookingForm(request.POST)
        if booking_form.is_valid():

            booking=booking_form.save(commit=False)
            booking.user=request.user
            booking.save()
            messages.success(request, "Booking successful!") 
    else:
        booking_form = TableBookingForm()

    #print("Rendering form")  #
    return render(request, 'booking.html', {'booking_form': booking_form})

def delete_user_old_bookings(request):
    """
    Delete old bookings for logged in user
    """
    all_bookings = TableBooking.objects.filter(user=request.user)
    deleted_bookings=[]
    for booking in all_bookings:
        if booking.booking_date < date.today():
            booking.delete()
            deleted_bookings.append(booking)
    return deleted_bookings

def user_booking_list(request):
    """
    List all bookings made by the logged-in user.
    """
    all_bookings = TableBooking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': all_bookings})

@login_required
def user_booking_update(request, id):
    """
    Update an existing booking.
    """
    booking = get_object_or_404(TableBooking, id=id, user=request.user)
    
    if request.method == 'POST':
        form = TableBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Successfully")
            return redirect("user_booking_list")  # Ensure this matches your URL name for the booking list view
    else:
        form = TableBookingForm(instance=booking)
    
    return render(request, "booking_update.html", {'form': form})

"""
def user_booking_update(request,id):
    
   # Update an existing booking.

    all_bookings = TableBooking.objects.get(id=id)
    if request.method=="POST":
        new_date=request.POST['booking_date']
        new_time=request.POST['booking_time']
        new_table=request.POST['table']
        new_guests=request.POST['number_of_guests']
        new_phone=request.POST['phone_number']
        new_special_request=request.POST['special_requests']

        all_bookings.booking_date=new_date
        all_bookings.booking_time=new_time
        all_bookings.table=new_table
        all_bookings.number_of_guests=new_guests
        all_bookings.phone_number=new_phone
        all_bookings.special_requests=new_special_request

        all_bookings.save()
        messages.success(request,"Updated Successfully")
        return redirect("booking")

    return render(request,"booking_update.html",{'form':all_bookings})


#def user_booking_delete(request):

"""
