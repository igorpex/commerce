from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.http import JsonResponse

from .models import User, Post, Follow, Like



def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post (request):
    return render(request, "network/index.html")


def view_posts(request, type):
    
    # Filter emails returned based on mailbox
    if type == "all":
        posts = Post.objects.all()
    elif type == "following":
        user = request.user

        values = Follow.objects.filter(follower__contains=user.id).values_list('pk', flat=True)
        posts = Post.objects.filter(author__in=list(values))
    
        # authors = User.objects.filter(follower = user)
        # posts = Post.objects.filter(
        #     author = authors
        # )
    
    else:
        return JsonResponse({"error": "Invalid type of posts."}, status=400)

    # Return posts in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

    # return render(request, "network/index.html")


def post(request, post_id):
    return render(request, "network/index.html")


def test_view_profile (request, username):
    profile_user = User.objects.get(username = username)
    try:
        is_following = Follow.objects.get(follower=request.user, author=profile_user)
        is_following = True
    except:
        is_following = False
    props = {
        "profile_user": profile_user, "is_following": is_following,
    }
    return render(request, "network/profile.html", props)


def test_view_post (request, post_id):
    post = Post.objects.get(id = post_id)
    
    try:
        my_like = Like.objects.get(post_id=post_id, liker = user)
        my_like = True
    except: 
        my_like = True
    props = {
        "post": post,
        "my_like": my_like,
    }
    return render(request, "network/post.html", props)
    


def test_view_posts (request, type):
    # Filter emails returned based on mailbox
    user = request.user
    if type == "all":
        posts = Post.objects.all()
    elif type == "following":
        follows = Follow.objects.filter(follower=user)
        u = User.objects.filter(id__in=[f.author.id for f in follows])
        posts = Post.objects.filter(author__in=u)

        # # user_id = user.id
        
        # # blog__name__in=inner_qs
        
        # posts = Post.objects.filter(author__in = user.followers.author.all())
    else:
        return JsonResponse({"error": "Invalid type of posts."}, status=400)

    my_likes = {}
    for post in posts:
        try:
            my_like = Like.objects.get(post_id=post.id, liker = user)
            if my_like:
                my_likes[post.id] = True
            else:
                my_likes[post.id] = False
        except:
            my_likes[post.id] = False

    # Return posts in reverse chronologial order
    # posts = posts.order_by("-timestamp").all()
    props = {
        "posts": posts,
        "my_likes": my_likes,
    }
    return render(request, "network/posts.html", props)
    # return JsonResponse([post.serialize() for post in posts], safe=False)


def test_follow (request, username):
    try:
        author = User.objects.get(username = username)
        follower = request.user
        if author == follower:
            return HttpResponse("<p>Can't follow yourself</p>")
        # new_follow = Follow(follower=follower, author=author)
        # new_follow.save()
        created  = Follow.objects.get_or_create(follower=follower, author=author)
        if created:
            return HttpResponse("<p>Follow created</p>")
        else:
            return HttpResponse("<p>Follow not created</p>")
    except:
        return HttpResponse("<p>Some error</p>")


def test_unfollow (request, username):
        author = User.objects.get(username = username)
        follower = request.user
        if author == follower:
            return HttpResponse("<p>Can't unfollow yourself</p>")
        # new_follow = Follow(follower=follower, author=author)
        # new_follow.save()
        try:
            old_follow = Follow.objects.get(follower=follower, author=author)
            if old_follow:
                old_follow.delete()
                return HttpResponse("<p>Unfollowed</p>")
        except:
            return HttpResponse("<p>Was not followed</p>")
    

def test_like (request, post_id):
    try:
        post = Post.objects.get(pk = post_id)
        liker = request.user
        if liker == post.author:
            return HttpResponse("<p>Can't like your own post</p>")
        # new_follow = Follow(follower=follower, author=author)
        # new_follow.save()
        like_created  = Like.objects.get_or_create(liker=liker, post=post)
        if like_created:
            return HttpResponse("<p>Like created</p>")
        else:
            return HttpResponse("<p>Like not created</p>")
    except:
        return HttpResponse("<p>Some error</p>")
        
    # post = Post.objects.get(id=post_id)
    # return HttpResponse(f"<p>{post.body} Liked</p>")

def test_unlike (request, post_id):
        post = Post.objects.get(pk = post_id)
        liker = request.user
        if liker == post.author:
            return HttpResponse("<p>Can't Unlike your own post</p>")
        # new_follow = Follow(follower=follower, author=author)
        # new_follow.save()
        try:
            old_like  = Like.objects.get(liker=liker, post=post)
            if old_like:
                old_like.delete()
                return HttpResponse("<p>Unliked</p>")
        except:
            return HttpResponse("<p>Was not liked</p>")

# def test_like_status(request):
