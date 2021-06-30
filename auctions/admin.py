from django.contrib import admin
# from django.contrib.auth.models import User  #new
# from django.contrib.auth.admin import UserAdmin #new

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "startprice", "status", "current_price", "creation_date", "creator")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "author", "price", "date")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "author", "text", "date")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "author", "price", "date")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
# Register your models here.

from .models import Listing, ListingStatus, Category, Watchlist, Comment, Bid
# from django.contrib.auth.models import User

admin.site.register(Listing, ListingAdmin)
admin.site.register(ListingStatus)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)

# admin.site.register(UserAdmin)


# Cancel defaultadmin model
# admin.site.unregister(User)

# register own admin on the  UserAdmin basis
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
    # pass