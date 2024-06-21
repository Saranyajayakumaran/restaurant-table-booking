from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class HomePageContent(models.Model):
    """
    Model to store the description and special offers of rhe restaurant
    """
    title=models.CharField(max_length=200)
    description=models.TextField()
    offers=models.TextField()

class ContactInformation(models.Model):
    address=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=15)
    email=models.EmailField()
    opening_hours=models.TextField()

    def __str__(self):
        return self.name


class MenuPageContent(models.Model):
    """
    Model to store the menu information of the restaurant eith price
    """
    name=models.CharField(max_length=300)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)


class TableInfo(models.Model):
    """
    The Table model is to store the informations about tables in the restaurant
    capacity and availability
    """
    table_number=models.PositiveIntegerField(unique=True)
    capacity=models.PositiveIntegerField()
    availability=models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_number} (Capacity:{self.capacity})"
 
class BookingTable(models.Model):
    """
    The Model to store the booking information
    Each booking is associated with user informations and table informations 
    """
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(TableInfo, on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    number_of_guests=models.PositiveIntegerField()
    special_requests=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Your Booking on {self.date} at {self.time} is confirmed"
