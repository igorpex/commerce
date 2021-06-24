from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .forms import CreateListingForm, CommentListingForm, BidForm
# from .forms import AddListingForm

from .models import Comment, Bid, Category, Watchlist, ListingStatus, Listing, User
from . import utils

def index(request):
    # status = ListingStatus.objects.get(id=4)
    status = ListingStatus.objects.get(status='open')
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


def view_listing(request, li_id):
    li = Listing.objects.get(id=li_id)
    #check authentication status
    if User.is_authenticated:

    # Function Watchlist

        # get current wathcing status
        is_watched = Watchlist.objects.filter(listing_id=li_id, watcher=request.user)
        
        # change watchlisted status if button clicked
        watch = request.GET.get("watch", "")
        # adding to watchlist
        if watch == 'add':
            if not is_watched:
                add_watched = Watchlist(listing_id=li_id, watcher =request.user)
                add_watched.save()
                is_watched = add_watched
        # removing from watchlist
        if watch == 'remove':
            if is_watched:
                is_watched.delete()

    # defaul view with no actions
    
    comments = Comment.objects.filter(listing=li)
    # price = utils.get_max_price(li_id)
    bids = Bid.objects.filter(listing=li)
    max_bid = bids.order_by('-price').first()
    if max_bid:
        if max_bid.price > li.startprice:
            price = max_bid.price
            if max_bid.author == request.user:
                your_bid = True
            else:
                your_bid = False
    else:
        price = li.startprice
        your_bid = False
        

    props = {
        'li':li,
        'is_watched': is_watched,
        'comments': comments,
        "comment_form": CommentListingForm(instance=li),
        "bid_form": BidForm,
        "bids": bids,
        "price": price,
        "your_bid": your_bid,
        # form = UserProfileEdit(instance=request.user)
        # 'bids':bids
        # 'message': message,
        }
    return render(request, "auctions/listing.html", props)


# Function to process Comments POST requests
def comment_listing(request, li_id):
    if request.method == "POST":
        comment_form = CommentListingForm(request.POST)
        # form = UserProfileEdit(instance=request.user)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.listing_id = li_id
            comment.save()
            redirect_path=reverse("auctions:view_listing", args=(li_id,))
            return HttpResponseRedirect(redirect_path)
    else:
        redirect_path=reverse("auctions:view_listing", args=(li_id,))
        return HttpResponseRedirect(redirect_path)

# Function to process Bid POST requests
def bid_listing (request, li_id):
    if request.method == "POST":
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            # if bid_form['price'] < price:
            # print(type(bid_form['price']))
            # original = bid_form._meta.model.objects.get(pk=bid_form.instance.pk)
            # print(original.price)
            form_price = bid_form.cleaned_data['price']
            # form.cleaned_data['my_field']
            # check maximum
            price = utils.get_max_price(li_id)
            if form_price <= price:
                redirect_path=reverse("auctions:view_listing", args=(li_id,))
                return HttpResponseRedirect(redirect_path)
            bid = bid_form.save(commit=False)
            bid.author = request.user
            bid.listing_id = li_id
            bid.save()
            redirect_path=reverse("auctions:view_listing", args=(li_id,))
            return HttpResponseRedirect(redirect_path)
    else:
        # redirect_path=reverse("auctions:view_listing", args=(li_id,))
        
        redirect_path=reverse("/", args=(li_id, ),)
        return HttpResponseRedirect(redirect_path)



# def import_categories(request):
#     for key in categories_options:
#         i = key
#         name = categories_options[key]
#         print(f'index: {i}, category {name}') 
#         c = Category(name=name, ebay_id=i)
#         # print(category)
#     return HttpResponseRedirect(reverse("auctions:index"))