from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime
from django.db.models import deletion
from django.db.models.aggregates import Max
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey
from django.utils.timezone import now

from django.contrib.auth.models import User

# to update listing current_price field
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    pass

class ListingStatus(models.Model):
    status = models.CharField(max_length=16)
    description = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.status}"


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=300, blank=True)
    ebay_id = IntegerField()

    def calculateOpenListings(self):
        status = ListingStatus.objects.get(status='open')
        return Listing.objects.filter(category=self, status=status,).count()

    listings = property(calculateOpenListings)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField()
    startprice = models.FloatField()
    photo = models.ImageField(upload_to='images/', blank=True)
    status = models.ForeignKey(ListingStatus, default=4, on_delete=models.PROTECT, related_name="statuses")
    imageurl = models.URLField(blank=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.PROTECT, related_name="categories", default=1)
    creation_date = models.DateTimeField(default=now, editable=False)
    creator = models.ForeignKey(User, default=None, blank=True, on_delete=models.PROTECT, editable=True)
    current_price = models.FloatField(blank=True, default=0)
    
    """this return startprice """
    def copy_start_price(self):
        return self.startprice

    """this copy startprice to current_price on the listing creation """
    def save(self, *args, **kwargs):
        if not self.current_price:
            self.current_price = self.copy_start_price()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Bid (models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, default=None, blank=True, on_delete=models.PROTECT, editable=True, related_name="bidders")
    price = models.FloatField()
    date = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.author.username} bid {self.price} to {self.listing.title}"

"""Update listing current_price on new bid save"""
@receiver(post_save, sender=Bid)
def update_listing_current_price(sender, instance, **kwargs):
    listing = Bid.objects.get(id=instance.id).listing
    listing.current_price = instance.price
    listing.save()

class Watchlist (models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watcher = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.watcher.username} watching: {self.listing.title}"


class Comment (models.Model):
    listing = models.ForeignKey(Listing, blank=True, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, default=None)
    date = models.DateTimeField(default=now, editable=False)
    author = ForeignKey(User, default=None, blank=True, on_delete=models.PROTECT, editable=True)
    def __str__(self):
        return f"{self.author.username} commented: {self.listing.title}"


