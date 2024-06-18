from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .models import HomePageContent
from .models import ContactInformation
from .models import MenuPageContent
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
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                user = User.objects.create_user(username=username, password=password, email=email)
                # Customer profile
                signup = SignupModel(user=user,email=email, phone_number=phone_number)
                signup.save()#save the datas
                #login(request, user)
                return redirect('login') 
            except IntegrityError:
                error_message = 'Username is already taken. Please choose a different username.'
                return render(request, 'signup.html', {'form': form, 'error_message': error_message})
    else:
        form = CustomerSignUpForm()
    return render(request, 'signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm

def loginpage(request):
    return render(request, 'login.html')