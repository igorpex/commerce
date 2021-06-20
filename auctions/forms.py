from django import forms
from django.forms.widgets import HiddenInput
from .models import *

from django.forms import ModelForm

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ('photo','creator', 'creation_date', 'status')
        success_url = 'auctions:index'
        