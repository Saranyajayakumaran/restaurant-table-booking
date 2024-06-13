from django.db import models

# Create your models here.

class HomePageContent(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    contact=models.TextField()
    offers=models.TextField()

    def __str__(self):
        return self.title