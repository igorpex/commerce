from django.shortcuts import render

from . import util

# New import
from django.http import HttpResponse


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
    return render(request, "encyclopedia/search.html", {
        "title": "Search Results",
        "entries": util.search(q)
    })

