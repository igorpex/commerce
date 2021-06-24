from django.contrib import admin
# from django.contrib.auth.models import User  #new
# from django.contrib.auth.admin import UserAdmin #new

# Register your models here.

from .models import Listing, ListingStatus, Category, Watchlist, Comment, Bid
# from django.contrib.auth.models import User

admin.site.register(Listing)
admin.site.register(ListingStatus)
admin.site.register(Category)
# admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Bid)

# admin.site.register(UserAdmin)


# Cancel defaultadmin model
# admin.site.unregister(User)

# register own admin on the  UserAdmin basis
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
    # pass