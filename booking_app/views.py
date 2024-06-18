from django.shortcuts import render
from django.http import HttpResponse
from .models import HomePageContent
from .models import ContactInformation
from .models import MenuPageContent
from .models import BookingTable
from .forms import BookingTableForm
from .forms import UserRegistrationForm

# Create your views here.
def homepage(request):
    content=HomePageContent.objects.first()
    contact_details=ContactInformation.objects.first()
    return render(request,'home.html',{'content':content,'contact_details':contact_details})

def menupage(request):
    menu_items=MenuPageContent.objects.all()
    return render(request,'menu.html',{'menu_items':menu_items})

#def booking(request):
 #   if request.method == 'POST':
  #      form = BookingTableForm(request.POST)
   #     if form.is_valid():
   #         form.save()
    #        return redirect('booking_app:booking_success')  # Redirect to a success page
   #     else:
   #         return render(request, 'booking.html', {'form': form})  # Re-render the form with errors
  #  else:
  #      form = BookingTableForm()
  #  return render(request, 'booking.html', {'form': form})  # Render the empty form for GET requests

#def booking_success(request):
    #return render(request, 'booking_success.html')

def booking(request):

    context={
        'bookingtableform':BookingTableForm()
    }
    return render(request,'booking.html',context)

def tablebooking(request):
    return render(request,'table_booking.html',{'tablebooking':tablebooking})

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    return render(request,"signin.html")

def signout(request):
    pass

