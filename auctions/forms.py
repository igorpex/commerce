from django import forms
from django.forms.widgets import HiddenInput
from .models import *

from django.forms import ModelForm

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        # exclude = ('photo','creator', 'creation_date', 'status')
        fields = ('title', 'description', 'startprice', 'imageurl', 'category')
        # success_url = 'auctions:index'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':'3'}),
            'startprice': forms.NumberInput(attrs={'class': 'form-control',}),
            'imageurl': forms.URLInput(attrs={'class': 'form-control',}),
            # 'category': forms.ModelChoiceField(queryset=Category.objects.all(), to_field_name="name"),
            }
        # widgets = {
        # 'description': forms.Textarea(attrs={'class': 'form-control', 'cols': 80, 'rows': 20}),
        # }

class CommentListingForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        # exclude = ('author', 'date', 'listing')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows':'3'}),
            }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ('price',)
        # exclude = ('author', 'date', 'listing')
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control',}),
            }