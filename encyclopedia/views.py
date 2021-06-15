from django.shortcuts import render

from . import util

# New import
from django.http import HttpResponse
from django import forms

from django.urls import reverse
from django.http import HttpResponseRedirect


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title of the page")
    title.widget.attrs.update({'class': 'form-control .form-group'})
    
    content = forms.CharField(label="Markdown content for the page", widget=forms.Textarea)
    content.widget.attrs.update({'class': 'form-control'})
    # form-control form-group


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": util.get_entry(title)
    })

def search(request):
    q = request.GET.get("q")
    entries = util.list_entries()
    if q.lower() in [entry.lower() for entry in entries]:
        return render(request, "encyclopedia/entry.html", {
            "title": q,
            "entry": util.get_entry(q)
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
                # return render(request, "encyclopedia/entry.html", {
                #     "title": title,
                #     "entry": util.get_entry(title)
                #  })
                #  redirect
            # return render(request, "encyclopedia/add.html", {"title": "Create Encyclopedia Entry", "form": form})
    else:
        return render(request, "encyclopedia/add.html", {"title": "Create Encyclopedia Entry", "form": NewEntryForm})