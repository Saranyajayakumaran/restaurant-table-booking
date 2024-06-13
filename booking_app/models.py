from django.db import models

# Create your models here.

class HomePageContent(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    offers=models.TextField()

    def __str__(self):
        return self.title
    
class ContactInformation(models.Model):
    address=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=30)
    email=models.EmailField()
    opening_hours=models.TextField()

    def __str__(self):
        return self.address