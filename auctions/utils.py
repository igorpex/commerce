import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .models import *

# def get_open_listings(status = 'open'):
#     # status = (ListingStatus.objects.get(status='open')) if status None
#     status = ListingStatus.objects.get(id=4)
#     # print(status)
#     listings = Listing.objects.filter(status=status)
#     print(listings[1].title)
#     print(listings[1].description)
#     return listings

def get_creators_listings(creator, status = 'open'):
    listings = Listing.objects.get(status='open')
    return listings

def get_category_listings(category_id):
  # status = (ListingStatus.objects.get(status='open')) if status None
  category = (Category.objects.get(id=category_id))
  listings = Listing.objects.get(ListingStatus='open', category=category)
  return listings

def get_max_price(li_id):
  li = Listing.objects.get(id=li_id)
  bids = Bid.objects.filter(listing=li)
  max_bid = bids.order_by('-price').first()
  if max_bid:
      if max_bid.price > li.startprice:
          price = max_bid.price
  else:
      price = li.startprice
  return price