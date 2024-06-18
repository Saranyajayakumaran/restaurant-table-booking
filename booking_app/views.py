from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import HomePageContent
from .models import ContactInformation
from .models import MenuPageContent
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import CustomerSignUpForm
from .models import SignupModel


# Create your views here.
def homepage(request):
    content=HomePageContent.objects.first()
    contact_details=ContactInformation.objects.first()
    return render(request,'home.html',{'content':content,'contact_details':contact_details})

def menupage(request):
    menu_items=MenuPageContent.objects.all()
    return render(request,'menu.html',{'menu_items':menu_items})

def signup_view(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            # Create the User object
            user = User.objects.create_user(username=username, password=password, email=email)
            # Create the Customer profile
            signup = SignupModel(user=user,email=email, phone_number=phone_number)
            signup.save()
            # Log the user in
            login(request, user)
            # Redirect to homepage or a success page
            return redirect('login')  # Replace 'home' with your actual URL name for the homepage
    else:
        form = CustomerSignUpForm()
    return render(request, 'signup.html', {'form': form})



def loginpage(request):
    return render(request,'login.html')