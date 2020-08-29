from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("categories/", views.all_categories, name="allCategories"),
    path("categories/<str:title_cat>/", views.categories, name="categories"),
    path("listings/<int:id_listing>/", views.listings, name="listings"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist_index/<int:id_listing>", views.watchlist_index, name="watchlistIndex"),
    path("watchlist_listing/<int:id_listing>", views.watchlist_listing, name="watchlistListing"),
    path("watchlist_watchlist/<int:id_listing>", views.watchlist_watchlist, name="watchlistWatchlist"),
    path("add_comment/<int:id_listing>", views.add_comment, name="addComment"),
    path("add_bet/<int:id_listing>", views.add_bet, name="addBet"),
    path("close_auction/<int:id_listing>", views.close_auction, name="closeAuction"),
    path("winlist/", views.win_list, name="winlist")

]
