from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, close_old_connections
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import CreateListingForm, CommentListingForm, BidForm

from .models import Comment, Bid, Category, Watchlist, ListingStatus, Listing, User
from . import utils
from django.contrib import messages



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        next = request.POST.get('next')
        if user is not None:
            login(request, user)
            if not next:
                return HttpResponseRedirect(reverse("auctions:index"))
            return HttpResponseRedirect(next) #redirect to next page
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                "next": next, #save redirect page in case wrong login
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

        next = request.POST.get('next')

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                "next": next,
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "next": next,
            })
        login(request, user)
        if not next:
            return HttpResponseRedirect(reverse("auctions:index"))
        return HttpResponseRedirect(next) #redirect to next page
    else:
        return render(request, "auctions/register.html")

"""Index page - view all open listings"""
def index(request):
    status = ListingStatus.objects.get(status='open')
    lis = Listing.objects.filter(status=status)

    return render(request, "auctions/index.html", {
                "lis": lis
            })


"""View Listing Item"""
def view_listing(request, li_id):
    """default props"""
    
    bid_message = None
    can_close = False

    """POST BID"""
    if request.method == "POST" and ('bid' in request.POST):
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            """check maximum"""
            form_price = bid_form.cleaned_data['price']
            current_price = utils.get_current_price(li_id)

            if form_price <= current_price:
                bid_message = 'bid must be more than current price'
            else: 
                bid = bid_form.save(commit=False)

                """ add required parameters to bid"""
                bid.author = request.user
                bid.listing_id = li_id

                """saving to bids and Listing.current_price"""
                bid.save()

    """defaul view with no actions"""

    """Get listing item by ID"""
    li = Listing.objects.get(id=li_id)

    """Get Watchlist button status"""
    #check authentication status
    if request.user.is_authenticated:
        is_watched = Watchlist.objects.filter(listing_id=li_id, watcher=request.user)   
    else:
        is_watched = False

    """ Process Watching change requests (add to watchlist, unwatch) """
    if request.user.is_authenticated:
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
    

    """Get Comments list"""
    comments = Comment.objects.filter(listing=li).order_by('-date')

    """Get bids for listing"""
    bids = Bid.objects.filter(listing=li)

    """Current price based on max bid and li.startprice"""
    current_price = utils.get_current_price(li_id)

    """Checks if your bid is current based on bid and request.user"""
    user = request.user
    your_bid_is_current = utils.get_your_bid_is_current(li_id, user)

    """checks if user can bid"""
    author = li.creator
    if request.user.is_authenticated:
        if request.user == author or li.status.status == 'closed':
            can_bid = False
        else:
            can_bid = True
    else:
        can_bid = False
    
    """checks if user is listing author and so can close the bid"""
    author = li.creator
    if request.user.is_authenticated:
        if request.user == author:
            can_close = True
        else:
            can_close = False

    """checks the winner"""
    
    if li.status.status == "closed":
        winner = utils.get_winner (li_id)
    else:
        winner = "No winner"

    
    """Props and render """
    props = {
        'li':li,
        'is_watched': is_watched,
        'comments': comments,
        "comment_form": CommentListingForm(instance=li),
        "bid_form": BidForm,
        "bids": bids,
        "current_price": current_price,
        "your_bid_is_current": your_bid_is_current,
        "can_bid": can_bid,
        "can_close": can_close,
        "winner": winner,
        "bid_message": bid_message,
        }

    return render(request, "auctions/listing.html", props)


"""POST Comment"""
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

"""POST Bid"""
def bid_listing (request, li_id):
    if request.method == "POST":
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            """check maximum"""
            form_price = bid_form.cleaned_data['price']
            current_price = utils.get_current_price(li_id)

            if form_price <= current_price:
                # bid_message = 'bid is to small'
                redirect_path=reverse("auctions:view_listing", args=(li_id, ))
                return HttpResponseRedirect(redirect_path)

            bid = bid_form.save(commit=False)

            """ add required parameters to bid"""
            bid.author = request.user
            bid.listing_id = li_id

            """saving to bids and Listing.current_price"""
            # try:
            bid.save()
            # except Exception as e: 
            #     print('Error on bid save:', e)
                # bid_error_message = 'bid_save_error'
            redirect_path=reverse("auctions:view_listing", args=(li_id, ))
            return HttpResponseRedirect(redirect_path)

            # else:
            #     Listing.objects.filter(id=li_id).update(current_price = form_price)
            
            redirect_path=reverse("auctions:view_listing", args=(li_id,))
            return HttpResponseRedirect(redirect_path)
    else:
        # redirect_path=reverse("auctions:view_listing", args=(li_id,))
        
        redirect_path=reverse("/", args=(li_id, ),)
        return HttpResponseRedirect(redirect_path)

"""Close Auction"""
def close_auction (request, li_id):
    if request.method == "POST":
        close_auction = request.POST['close_auction']
        if close_auction:
            """Update listing status"""
            li = Listing.objects.get(id=li_id)
            status = ListingStatus.objects.get(status="closed")
            li.status = status
            li.save()

            """redirect to listing page"""
            redirect_path=reverse("auctions:view_listing", args=(li_id, ))
            return HttpResponseRedirect(redirect_path)

            # li.winner = 

"""Create new listing"""
@login_required
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


"""View user's Watchlist"""
@login_required
def watchlist(request):
    status = ListingStatus.objects.get(id=4)
    user_id = request.user.id
    lis = Listing.objects.filter(status=status, watchlist__watcher=user_id)
    return render(request, "auctions/watchlist.html", {
                "lis": lis
            })


"""View user's created listings"""
@login_required

def my_listings(request):
    user = request.user
    lis = Listing.objects.filter(creator=user.id)
    

    for li in lis:
        """for closed listings"""
        if li.status.status == "closed":
            li_status = "closed"
            """for open listings"""
        elif li.status.status == "open":
            li_status = "open"
        
        # my_status_dict[li.id] = my_status
        li.li_status = li_status

    return render(request, "auctions/mylistings.html", {
            "lis": lis, "li_status": li_status,
        })

"""View all participated listings (where user bid)"""
@login_required
# @login_required(redirect_field_name='auctions:watchlist')
def my_bid_listings(request):

    user = request.user
    user_id = user.id

    """Checks all bidded listings"""

    # get all participated listings
    lis = Listing.objects.filter(bid__author = user_id).distinct()
    
    """Get statuses for listings"""

    user = request.user
    for li in lis:
        """for closed listings"""
        if li.status.status == "closed":
            """Checks if your bid is current based on bid and request.user"""
            my_bid_is_current = utils.get_your_bid_is_current(li.id, user)
            if my_bid_is_current:
                my_status = "won"
            else:
                my_status = "lost"

            """for open listings"""
        elif li.status.status == "open":
            my_bid_is_current = utils.get_your_bid_is_current(li.id, user)
            if my_bid_is_current:
                my_status = "current"
            else:
                my_status = "not current"
        elif li.creator == user:
            my_status = "my listing"
        else:
            my_status = "status unknown"
        
        li.my_status = my_status    
    
    return render(request, "auctions/my-bid-listings.html", {
                "lis": lis,
            })


"""View Categories List"""
def view_categories(request):
    categories = Category.objects.all()
    status = ListingStatus.objects.get(status='open')
    count_all = Listing.objects.filter(status=status).count()
    return render(request, "auctions/categories.html", {"categories": categories, "count_all": count_all})


"""View Listings of exact category"""
def view_category(request, category_id):
    status = ListingStatus.objects.get(status='open')
    category = (Category.objects.get(id=category_id))
    """for category All Categories(id 1)"""
    if category_id == 1:
        lis = Listing.objects.filter(status=status)
        return render(request, "auctions/category.html", {"lis": lis, "category": category})
        """for other Categories"""
    else:
        lis = Listing.objects.filter(status=status, category=category)
    return render(request, "auctions/category.html", {"lis": lis, "category": category})


# def import_categories(request):
#     for key in categories_options:
#         i = key
#         name = categories_options[key]
#         print(f'index: {i}, category {name}') 
#         c = Category(name=name, ebay_id=i)
#         # print(category)
#     return HttpResponseRedirect(reverse("auctions:index"))