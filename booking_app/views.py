from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import authenticate,login
from .models import HomePageContent
from .models import ContactInformation
from .models import MenuPageContent
from .forms import CustomerSignUpForm
from .forms import CustomerLoginForm
#from .models import SignupModel


# Create your views here.
def homepage(request):
    content=HomePageContent.objects.first()
    contact_details=ContactInformation.objects.first()
    return render(request,'home.html',{'content':content,'contact_details':contact_details})

def menupage(request):
    menu_items=MenuPageContent.objects.all()
    return render(request,'menu.html',{'menu_items':menu_items})

##SignUp
def signup_view(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = CustomerSignUpForm()
    return render(request, 'signup.html', {'form': form})


## LogIn

def login_view(request):
    if request.method=="POST":
        form=CustomerLoginForm(request.POST)

        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse("<h1>Login successfull<h2>")
                else:
                    return HttpResponse("<h1> Disable Account <h1>")
            else:
                return HttpResponse("<h1>Invalid login</h1>")
    else:
        form=CustomerLoginForm()
    return render(request,'login',{"form:form"})
            

