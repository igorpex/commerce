from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "body", "author")

# Register your models here.

from .models import Post, Follow, Like
# from django.contrib.auth.models import User

admin.site.register(Post, PostAdmin)
admin.site.register(Follow)
admin.site.register(Like)