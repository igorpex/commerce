from django import forms
from django.forms.widgets import HiddenInput
from .models import *

from django.forms import ModelForm


# class AddListingForm(forms.Form):
#     title = forms.CharField(label="Title", help_text="Enter name of the listing", widget=forms.TextInput(attrs={'class': 'title'}))
#     description = forms.CharField(label="Title", help_text="Enter name of the listing", widget=forms.Textarea(attrs={'class': 'description'}))
#     startprice = forms.Textarea()
#     status = ListingStatus.objects.get(status)
#     imageurl = forms.URLField()
#     category = Category.objects.get()


class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ('photo','creator', 'creation_date', 'status')
        # status = models.ForeignKey(ListingStatus, on_delete=models.PROTECT, related_name="statuses")
        # status = ListingStatus.objects.get(status = 'open', HiddenInput=True)
        success_url = 'auctions:index'
        