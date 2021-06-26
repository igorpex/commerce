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

# def get_max_price(li_id):
#   li = Listing.objects.get(id=li_id)
#   bids = Bid.objects.filter(listing=li)
#   max_bid = bids.order_by('-price').first()
#   if max_bid:
#       if max_bid.price > li.startprice:
#           price = max_bid.price
#   else:
#       price = li.startprice
#   return price

def get_current_price(li_id):
    li = Listing.objects.get(id=li_id)
    bids = Bid.objects.filter(listing=li)
    max_bid = bids.order_by('-price').first()

    if max_bid: #if filter provided results
        if max_bid.price > li.startprice: #doublecheck
            current_price = max_bid.price
    else:
        current_price = li.startprice
    return current_price


def get_your_bid_is_current(li_id, user):
    li = Listing.objects.get(id=li_id)
    bids = Bid.objects.filter(listing=li)
    max_bid = bids.order_by('-price').first()
    if max_bid:
        if max_bid.author == user:
                return True
        else:
            return False
    else:
        return False
    return False

# def ged_max_bid_author(li_id):
#   li = Listing.objects.get(id=li_id)
#   bids = Bid.objects.filter(listing=li)
#   max_bid = bids.order_by('-price').first()
  

def get_winner (li_id):
    li = Listing.objects.get(id=li_id)
    bids = Bid.objects.filter(listing=li)
    max_bid = bids.order_by('-price').first()
    if max_bid:
        return max_bid.author.username
    else:
        return "No Winner"

"""Used to update database then added new field"""
def copy_price():
    from .models import Listing
    lis = Listing.objects.all()
    for li in lis:
        li.current_price = li.startprice
        li.save()
        print(f'updated: {li.title}')