from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    # path("import", views.import_categories, name="import_categories"),
    # path("listings/<int:li_id>", views.view_listing, name="view_listing"),
    path("listings/<int:li_id>/", views.view_listing, name="view_listing"),
    path("listings/<int:li_id>/comment/", views.comment_listing, name="comment_listing"),
    path("listings/<int:li_id>/bid/", views.bid_listing, name="bid_listing"),
    path("listings/", views.index, name="listings"),
]
