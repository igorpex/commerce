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

from django.core.exceptions import ValidationError

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
    ebay_id = IntegerField()

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
    # creator = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.PROTECT, editable=False)
    # creation_date = models.DateTimeField(default=datetime.now, blank=True)
    # creator = models.ForeignKey(User, default=User.username, editable=False, on_delete=models.PROTECT)
    # creator = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    # creator = models.ForeignKey(User, default=User, editable=False, on_delete=models.PROTECT)
    # watched_by = models.ManyToManyField("User", related_name="watched_listings")
    
    def copy_start_price(self):
        return self.startprice
    
    def save(self, *args, **kwargs):
        if not self.current_price:
            self.current_price = self.copy_start_price()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title



# @receiver(post_save, sender=Bid)
# def update_calculated_fields(sender, instance, **kwargs):
#     current_price = instance.price
#     sender.objects.filter(pk=instance.pk).update(current_price=current_price)

# Сигнал, если товар сохранился со скидкой, то пересохраняем цены у размеров
# @receiver(post_save, sender=Product)
# def update_price_for_size(sender, instance, **kwargs):
#         product = Product.objects.get(name=instance)
#         savesize = Sizes.objects.filter(product=product)
#         for ss in savesize:
#                 ss.save()




class Watchlist (models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watcher = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.watcher.username} watching: {self.listing.title}"

class Bid (models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, default=None, blank=True, on_delete=models.PROTECT, editable=True)
    price = models.FloatField()
    date = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"{self.author.username} bid {self.price} to {self.listing.title}"
    
    # def clean_fields(self, exclude=None):
    #     super().clean_fields(exclude=exclude)
    #     # li = self.listing
    #     raise ValidationError(('Too small')
    #     )
            
        # bids = Bid.objects.filter(listing=li)
        # max_bid = bids.order_by('-price').first()
        # if max_bid:
        #     if self.price <= max_bid is not None:
        #         raise ValidationError(
        #             _('Too small')
        #             )

"""Update listing current_price on new bid save"""
@receiver(post_save, sender=Bid)
def update_listing_current_price(sender, instance, **kwargs):
    listing = Bid.objects.get(id=instance.id).listing
    listing.current_price = instance.price
    listing.save()


class Comment (models.Model):
    listing = models.ForeignKey(Listing, blank=True, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, default=None)
    date = models.DateTimeField(default=now, editable=False)
    author = ForeignKey(User, default=None, blank=True, on_delete=models.PROTECT, editable=True)
    def __str__(self):
        return f"{self.author.username} commented: {self.listing.title}"
