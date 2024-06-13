from django.shortcuts import render
from django.http import HttpResponse
from .models import HomePageContent

# Create your views here.
def homepage(request):
    content=HomePageContent.objects.first()
    return render(request,'home.html',{'content':content})