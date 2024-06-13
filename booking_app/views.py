from django.shortcuts import render
from django.http import HttpResponse
from .models import HomePageContent
from .models import ContactInformation
from .models import MenuPageContent

# Create your views here.
def homepage(request):
    content=HomePageContent.objects.all()
    contact_details=ContactInformation.objects.all()
    return render(request,'home.html',{'content':content,'contact_details':contact_details})

def menupage(request):
    content=MenuPageContent.objects.all()
    return render(request,'menu.html',{'content':content})