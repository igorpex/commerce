from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime
from django.utils.timezone import now

from django.contrib.auth.models import User

from django.conf import settings


class User(AbstractUser):
    pass


class ListingStatus(models.Model):
    status = models.CharField(max_length=16)
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.status}"

class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=300)

    def __str__(self):
        return f"id = {self.id} {self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    startprice = models.FloatField()
    photo = models.ImageField(upload_to='images/', blank=True)
    status = models.ForeignKey(ListingStatus, default=4, on_delete=models.PROTECT, related_name="statuses")
    imageurl = models.URLField(blank=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.PROTECT, related_name="categories", default=1)
    # creation_date = models.DateTimeField(default=datetime.now, blank=True)
    creation_date = models.DateTimeField(default=now, editable=False)
    # creator = models.ForeignKey(User, default=User.username, editable=False, on_delete=models.PROTECT)
    # creator = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    # creator = models.ForeignKey(User, default=User, editable=False, on_delete=models.PROTECT)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.PROTECT, editable=False)
    
    def __str__(self):
        return self.title
    

