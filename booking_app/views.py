from django.shortcuts import render
from django.http import HttpResponse
from .models import HomePageContent
from .models import ContactInformation
from .models import MenuPageContent

# Create your views here.
def homepage(request):
    content=HomePageContent.objects.first()
    contact_details=ContactInformation.objects.first()
    return render(request,'home.html',{'content':content,'contact_details':contact_details})

def menupage(request):
    menu_items=MenuPageContent.objects.all()
    contact_details=ContactInformation.objects.first()
    content = HomePageContent.objects.first()
    return render(request,'menu.html',{'menu_items':menu_items,'contact_details':contact_details,'title':content.title if content else 'Restaurant'})