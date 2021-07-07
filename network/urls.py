
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


# API Routes
    path("posts/new", views.new_post, name="new_post"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("posts/<str:type>", views.view_posts, name="view_posts"),

# Test views
    path("test/profile/<str:username>", views.test_view_profile, name="test_view_profile"),
    path("test/posts/<str:type>", views.test_view_posts, name="test_view_posts"),
    path("test/post/<int:post_id>", views.test_view_post, name="test_view_post"),
    path("test/follow/<str:username>", views.test_follow, name="test_follow"),
    path("test/unfollow/<str:username>", views.test_unfollow, name="test_unfollow"),
    path("test/like/<int:post_id>", views.test_like, name="test_like"),
    path("test/unlike/<int:post_id>", views.test_unlike, name="test_unlike"),
]