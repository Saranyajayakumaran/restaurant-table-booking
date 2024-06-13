from django.contrib import admin
from .models import HomePageContent
from .models import ContactInformation

# Register your models here.
admin.site.register(HomePageContent)
admin.site.register(ContactInformation)