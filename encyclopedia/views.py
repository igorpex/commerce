from django.shortcuts import render

from . import util

# New import
from django.http import HttpResponse
from django import forms

from django.urls import reverse
from django.http import HttpResponseRedirect
import random


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title of the page")
    title.widget.attrs.update({'class': 'form-control'})
    
    content = forms.CharField(label="Markdown content for the page", widget=forms.Textarea)
    content.widget.attrs.update({'class': 'form-control'})


class NewEditForm(forms.Form):
    title = forms.CharField(label="Title of the page")
    # title.widget.attrs.update({'class': 'form-control'})
    content = forms.CharField(label="Markdown content for the page", widget=forms.Textarea)
    # content.widget.attrs.update({'class': 'form-control'})


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": util.get_html_entry(title)
    })

def search(request):
    q = request.GET.get("q")
    entries = util.list_entries()
    if q.lower() in [entry.lower() for entry in entries]:
        return render(request, "encyclopedia/entry.html", {
            "title": q,
            "entry": util.get_html_entry(q)
        })
    else:
        return render(request, "encyclopedia/search.html", {
            "title": "Search Results",
            "entries": util.search(q)
        })

def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            # check for unique
            entries = util.list_entries()
            unique = title.lower() not in [entry.lower() for entry in entries]

            # if title exist, give error
            if not unique:
                return render(request, "encyclopedia/add.html", {"title": "Create Encyclopedia Entry", "form": form, 'error':'This title is not unique, please change'})
            # if unique
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(f'../{title}')

    else:
        return render(request, "encyclopedia/add.html", {"title": "Create Encyclopedia Entry", "form": NewEntryForm})


def edit(request):
# checks that it is from entry page
    if request.method == "GET":
        entry = request.GET.get("entry") 
        # prepare form
        md = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html", {"title": "Edit Encyclopedia Entry", "entry": entry, "md":md})

    if request.method == "POST":
        entry = request.POST.get("entry")
        md = request.POST.get("md")
        util.save_entry(entry, md)

        return HttpResponseRedirect(f'../{entry}')


def random_page(request):
    entries = util.list_entries()
    entry = random.sample(entries, 1)[0]
    return HttpResponseRedirect(f'../{entry}')
    # alternate solution:
    # r = random.randint(1,len(entries)) - 1
    # return HttpResponseRedirect(f'../{entries[r]}')