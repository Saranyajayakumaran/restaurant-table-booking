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
    context = {
        'menu_items': menu_items,
    }
    return render(request,'menu.html',context)