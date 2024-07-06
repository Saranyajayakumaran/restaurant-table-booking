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
    delete_user_old_bookings(request)

    #print("i am in booking page")
    if request.method == 'POST':
        booking_form = TableBookingForm(request.POST)
        if booking_form.is_valid():

            booking=booking_form.save(commit=False)
            booking.user=request.user
            booking.save()
            messages.success(request, "Thank you for booking with us!")
        else:
            messages.error(request, "Please correct the Field below.")
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

@login_required
def user_booking_list(request):
    """
    List all bookings made by the logged-in user.
    """
    all_bookings = TableBooking.objects.filter(user=request.user)
    return render(request, 'booking_list.html', {'bookings': all_bookings})


def user_booking_update(request,id):
    """
    Update an existing booking.
    """
    booking = get_object_or_404(TableBooking, id=id, user=request.user)
    
    if request.method == 'POST':
        form = TableBookingForm(request.POST, instance=booking)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, "Updated Successfully")
                #return redirect("user_booking_update") #redirect to same page
    else:
        form = TableBookingForm(instance=booking)
    return render(request, "booking_update.html", {'form': form})


def user_booking_delete(request,id):
    """
    Delete the selected existing  booking.
    """
    booking = get_object_or_404(TableBooking, id=id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking deleted successfully.")
        return redirect('user_booking_list')
    
    #return render(request, "delete.html",)
    







