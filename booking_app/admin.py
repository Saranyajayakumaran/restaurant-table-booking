"""
Standard and third party imports
"""
from django.contrib import admin
from .models import HomePageContent
from .models import MenuPageContent
from .models import TableInfo,TableBooking

# Register your models here.
admin.site.register(HomePageContent)
admin.site.register(MenuPageContent)
admin.site.register(TableInfo)
admin.site.register(TableBooking)
