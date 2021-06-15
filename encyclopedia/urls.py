from django.urls import path

from . import views

# app_name = "encyclopedia" - this breaks things
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.get_entry, name="entry")
]
