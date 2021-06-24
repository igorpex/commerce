from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .forms import CreateListingForm
# from .forms import AddListingForm

from .models import *

from . import utils

from .categories_options import categories_options

def index(request):
    status = ListingStatus.objects.get(id=4)
    # print(status)
    lis = Listing.objects.filter(status=status)
    # print(listings[1].title)
    # print(listings[1].description)
    # listings = utils.get_open_listings()
    return render(request, "auctions/index.html", {
                "lis": lis
            })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.creator = request.user
            instance.save()
            # messages.success(request, f'Listing Adde')
            return HttpResponseRedirect(reverse("auctions:index"))
        # else:
            # return render(request, "auctions/create.html", {"form": form})
    else:
        return render(request, "auctions/create.html", {"form": CreateListingForm})


def category_listings(request):
    category_id = request.GET["category_id"]
    utils.get_category_listings(category_id)



def watchlist(request):
    status = ListingStatus.objects.get(id=4)
    # username=request.user.username
    user_id = request.user.id
    # print(username)
    lis = Listing.objects.filter(status=status, watchlist__watcher=user_id)
    # Product.objects.filter(company__name="Apple")
    # print(listings[1].title)
    # print(listings[1].description)
    # listings = utils.get_open_listings()
    return render(request, "auctions/watchlist.html", {
                "lis": lis
            })


def import_categories(request):
    for key in categories_options:
        i = key
        name = categories_options[key]
        print(f'index: {i}, category {name}') 
        c = Category(name=name, ebay_id=i)
        # print(category)
    return HttpResponseRedirect(reverse("auctions:index"))


def view_listing(request, li_id):
    try:
        li = Listing.objects.get(id=li_id)
        #check authentication status
        if User.is_authenticated:

            # check current wathcing status
            # is_watched = Watchlist.objects.filter(listing_id=li_id, watcher__username=request.user.username)
            is_watched = Watchlist.objects.filter(listing_id=li_id, watcher=request.user)  
            # if is_watched:
            #     message = 'is_watched'
            # else:
            #     message = 'not_watched'

            # check click on button "Add to watchlist" or "Unwatch"
            redirect_path = f'{reverse("auctions:index")}/{li.id}/'

            watch = request.GET.get("watch", "")
            
            # add case
            if watch == 'add':
                if is_watched:
                    props = {
                        'li':li,
                        'is_watched': is_watched, #to show "Add to watchist" or "Watched and Unwatch"
                        'message': "Already in watchlist",
                        }
                    # HttpResponseRedirect(redirect_path)
                    return render(request, "auctions/listing.html", props)
                else:
                    add_watched = Watchlist(listing_id=li_id, watcher =request.user)
                    add_watched.save()
                    is_watched = add_watched
                    props = {
                        'li':li,
                        'is_watched': is_watched,
                        'message': "Added to watchlist",
                    }
                    # HttpResponseRedirect(redirect_path)
                    return render(request, "auctions/listing.html", props)
            
            # remove case
            if watch == 'remove':
                if is_watched:
                    is_watched.delete()
                    is_watched = False
                    props = {
                        'li':li,
                        'is_watched': is_watched, #to show "Add to watchist" or "Watched and Unwatch"
                        # 'message': "Removed from Whitelist",
                        }
                    # HttpResponseRedirect(redirect_path)
                    return render(request, "auctions/listing.html", props)

                else:
                    # print('Removed twice')
                    props = {
                    'li':li,
                    'is_watched': is_watched, #to show "Add to watchist" or "Watched and Unwatch"
                    # 'message': "Already removed",
                    }
                    return render(request, "auctions/listing.html", props)
                    # HttpResponseRedirect(redirect_path)
                    
        # case with no actions
        props = {
            'li':li,
            'is_watched': is_watched, #to show "Add to watchist" or "Watched and Unwatch"
            # 'message': message,
            }
        return render(request, "auctions/listing.html", props)
    except:
        raise Http404
        # return HttpResponseRedirect(reverse("auctions:index"))
        # Watchlist block


