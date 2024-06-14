from django.contrib import admin
from .models import HomePageContent
from .models import ContactInformation
from .models import MenuPageContent
from .models import BookingForm

# Register your models here.
admin.site.register(HomePageContent)
admin.site.register(ContactInformation)
admin.site.register(MenuPageContent)
admin.site.register(BookingForm)