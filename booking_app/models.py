from django.db import models
from django.contrib.auth.models import User
#from django.core.exceptions import ValidationError
#from django.utils import timezone


# Create your models here.
class SignUpModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
   

class HomePageContent(models.Model):
    """
    Model to store the description and special offers of rhe restaurant
    """
    offers=models.TextField()

#class ContactInformation(models.Model):
    #address=models.CharField(max_length=200)
    #phone_number=models.CharField(max_length=15)
    #email=models.EmailField()
    #opening_hours=models.TextField()


class MenuPageContent(models.Model):
    """
    Model to store the menu information of the restaurant eith price
    """
    name=models.CharField(max_length=300)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)


class TableInfo(models.Model):
    """
    The Table model is to store the informations about tables in the restaurant by admin
    capacity and availability
    """
    table_number=models.PositiveIntegerField(unique=True)
    seats=models.IntegerField()

    def __str__(self):
        return f"Table {self.table_number} (Seats:{self.seats})"
 
class TableBooking(models.Model):
    """
    The Model to store the booking information
    Each booking is associated with user informations and table informations 
    """
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(TableInfo, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    phone_number=models.CharField(max_length=15,blank=True,null=True,help_text='optional')
    number_of_guests=models.PositiveIntegerField()
    special_requests=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.user} has booked {self.table} on {self.booking_date} at {self.booking_time}"
		