from django.urls import path

from . import views

# app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.get_entry, name="entry"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add")
]
