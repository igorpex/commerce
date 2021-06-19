from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class ListingStatus(models.Model):
    status = models.CharField(max_length=16)
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.status}"

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=1000)
    startprice = models.FloatField()
    photo = models.ImageField(upload_to='images/')
    status = models.ForeignKey(ListingStatus, on_delete=models.CASCADE, related_name="statuses")

    def __str__(self):
        return self.title
    

