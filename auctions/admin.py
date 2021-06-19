from django.contrib import admin

# Register your models here.

from .models import Listing, ListingStatus

admin.site.register(Listing)
admin.site.register(ListingStatus)
