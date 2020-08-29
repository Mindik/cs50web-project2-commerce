from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django import forms
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.defaulttags import register
from .models import User, Listings, Category, WatchList, Comments, Bet


# New filter for count category
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# Class for create listing form
class CreateListing(forms.Form):
    title = forms.CharField(label="", max_length=64, widget=forms.TextInput(attrs={"placeholder": "Title",
                                                                                   "class": "form-control"}))

    text = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder": "Text",
                                                                  "class": "form-control"}))

    price = forms.FloatField(label="", min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Price",
                                                                                    "class": "form-control"}))
    url = forms.URLField(label="", required=False,
                         widget=forms.URLInput(attrs={"placeholder": "URL for image", "class": "form-control"}))

    category = forms.MultipleChoiceField(label="", required=False,
                                         choices=[(choice.id, choice.cat) for choice in Category.objects.all()],
                                         widget=forms.SelectMultiple(attrs={"class": "form-control"}))


# Class for add comment in listing page
class AddComment(forms.Form):
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'rows': 3,
                                                                  "placeholder": "Text comment",
                                                                  "class": "form-control addComment col-6"}))


# Class for set bid in listing page
class SetBet(forms.Form):
    bet = forms.FloatField(label="", widget=forms.NumberInput(attrs={"placeholder": "Bet",
                                                                     "class": "form-control col-3 bet"}))


# Function for pagination
def pag(request, all_listings, count_listings):
    page_number = request.GET.get("page", 1)
    paginator = Paginator(all_listings, count_listings)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = f"?page={page.previous_page_number()}"
    else:
        prev_url = ""

    if page.has_next():
        next_url = f"?page={page.next_page_number()}"
    else:
        next_url = ""

    return page, is_paginated, prev_url, next_url


# Function for index
def index(request):
    # Get all open listings
    all_open_listings = Listings.objects.filter(open=True)
    # Paginate
    page_list = pag(request, all_open_listings, 3)
    # For active navigation button
    active = "index"
    # If the user is not logged in
    if not request.user.is_authenticated:
        return render(request, "auctions/index.html", {
            "page_objects": page_list[0], "is_paginated": page_list[1], "next_url": page_list[3],
            "prev_url": page_list[2], "active": active
        })
    else:
        # List for watched lists
        ls = [a.id_listing for a in WatchList.objects.filter(id_user=request.user)]

        return render(request, "auctions/index.html", {
            "page_objects": page_list[0], "count": len(WatchList.objects.filter(id_user=request.user)),
            "is_paginated": page_list[1], "next_url": page_list[3], "prev_url": page_list[2], "active": active,
            "count_win": len(Listings.objects.filter(win=request.user)), "ls": ls
        })


# Login function
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
            active = "login"
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.", "active": active
            })
    else:
        active = "login"
        return render(request, "auctions/login.html", {"active": active})


# Logout function
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register function
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            active = "register"
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.", "active": active
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            active = "register"
            return render(request, "auctions/register.html", {
                "message": "Username already taken.", "active": active
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        active = "register"
        return render(request, "auctions/register.html", {"active": active})


@login_required
def create(request):
    if request.method == "POST":
        # Get form data
        form = CreateListing(request.POST)
        if form.is_valid():
            # If the URL is not specified, then we use the default
            if not form.cleaned_data["url"]:
                url = "https://www.designthenewbusiness.com/wp-content/uploads/2011/09/moving_box1.jpg"
            else:
                url = form.cleaned_data["url"]
            new_listing = Listings(title=form.cleaned_data["title"], text_base=form.cleaned_data["text"],
                                   start_bid=form.cleaned_data["price"], url_img=url,
                                   author=request.user)
            new_listing.save()
            # We set the maximum bid equal to the starting one
            # and add it to the list of watched for the author of the list
            new_listing.set_max_bet(new_listing.start_bid)
            new_listing.add_win_list(request.user)
            new_listing.save()
            # If the category is not specified, then set by default
            if not form.cleaned_data["category"]:
                category = [16]
            else:
                category = form.cleaned_data["category"]
            new_listing.category.set(Category.objects.filter(pk__in=category))

            return HttpResponseRedirect(reverse("listings", args=[new_listing.id]))
    else:
        # Method "GET"
        active = "create"
        return render(request, "auctions/create.html", {
            "form": CreateListing(), "count": len(WatchList.objects.filter(id_user=request.user)), "active": active,
            "count_win": len(Listings.objects.filter(win=request.user))
        })


# Function for list categories
def all_categories(request):
    # Get all categories
    all_cat = Category.objects.all()
    # Paginate
    page_list = pag(request, all_cat, 5)
    # We form a dictionary for the number of lists in each category that are not yet closed
    open_watch = {}
    for a in all_cat:
        open_watch[a.cat] = len(a.category.filter(open=True))
    # For active navigation button
    active = "allCategories"
    if request.user.is_authenticated:
        return render(request, "auctions/allCategories.html", {
            "page_objects": page_list[0], "count": len(WatchList.objects.filter(id_user=request.user)),
            "active": active,
            "openWatch": open_watch, "is_paginated": page_list[1], "next_url": page_list[3], "prev_url": page_list[2],
            "count_win": len(Listings.objects.filter(win=request.user))
        })
    return render(request, "auctions/allCategories.html", {
        "page_objects": page_list[0], "active": active, "openWatch": open_watch, "is_paginated": page_list[1],
        "next_url": page_list[3],
        "prev_url": page_list[2]
    })


# Function for a list of one category
def categories(request, title_cat):
    # Get selected category
    cat = Category.objects.get(cat=title_cat)
    # Get all open listings in a given category
    all_cat = Listings.objects.filter(category=cat, open=True)
    # Paginate
    page_list = pag(request, all_cat, 3)

    if request.user.is_authenticated:
        # Generating a list of watched lists
        ls = [a.id_listing for a in WatchList.objects.filter(id_user=request.user)]
        return render(request, "auctions/categories_list.html", {
            "page_objects": page_list[0], "count": len(WatchList.objects.filter(id_user=request.user)),
            "title_cat": title_cat, "is_paginated": page_list[1], "next_url": page_list[3], "prev_url": page_list[2],
            "ls": ls, "count_win": len(Listings.objects.filter(win=request.user))
        })
    return render(request, "auctions/categories_list.html", {
        "page_objects": page_list[0], "title_cat": title_cat, "is_paginated": page_list[1], "next_url": page_list[3],
        "prev_url": page_list[2]
    })


def listings(request, id_listing):
    # Get listing
    listing = Listings.objects.get(id=id_listing)

    # Get comments for listing
    list_comments = Comments.objects.filter(id_listing=id_listing)
    # Get bet for listing
    list_bet = Bet.objects.filter(id_listing=id_listing)

    if request.user.is_authenticated:
        # Checking the list of watched
        delete = WatchList.objects.filter(id_listing=id_listing, id_user=request.user)
        # Forms for comments and bet
        form = AddComment()
        form_bet = SetBet()
        # Check if the user has made a bid
        # The user can only place 1 bet. Can comment many times
        check_bet_user = Bet.objects.filter(id_listing=id_listing, id_user=request.user)

        return render(request, "auctions/listing.html", {
            "listing": listing, "count": len(WatchList.objects.filter(id_user=request.user)), "del": delete,
            "listComments": list_comments, "form": form,
            "checkBetUser": check_bet_user, "formBet": form_bet, "countListBet": len(list_bet),
            "count_win": len(Listings.objects.filter(win=request.user))
        })
    return render(request, "auctions/listing.html", {
        "listing": listing, "listComments": list_comments
    })


# Function for watchlist
@login_required
def watchlist(request):
    # Get watchlist for user
    watchlist_user = WatchList.objects.filter(id_user=request.user)

    page_list = pag(request, watchlist_user, 3)

    active = "watchlist"
    ls = [a.id_listing for a in WatchList.objects.filter(id_user=request.user)]
    return render(request, "auctions/watchlist.html", {
        "page_objects": page_list[0], "count": len(WatchList.objects.filter(id_user=request.user)),
        "is_paginated": page_list[1], "next_url": page_list[3], "prev_url": page_list[2], "ls": ls,
        "active": active, "count_win": len(Listings.objects.filter(win=request.user))
    })


# The function of adding or removing from the tracked list
def add_remove_watchlist(request, id_listing):
    if len(WatchList.objects.filter(id_listing=id_listing, id_user=request.user)) == 0:
        WatchList(id_user=request.user, id_listing=Listings.objects.get(id=id_listing)).save()
    else:
        WatchList.objects.filter(id_listing=id_listing, id_user=request.user).delete()


# Three functions for adding or removing. Applied two routes due to returning to different pages
@login_required
def watchlist_index(request, id_listing):
    if request.method == "POST":
        add_remove_watchlist(request, id_listing)
        return HttpResponseRedirect(reverse("index"))


@login_required
def watchlist_listing(request, id_listing):
    if request.method == "POST":
        add_remove_watchlist(request, id_listing)
        return HttpResponseRedirect(reverse("listings", args=[id_listing]))


@login_required
def watchlist_watchlist(request, id_listing):
    if request.method == "POST":
        add_remove_watchlist(request, id_listing)
        return HttpResponseRedirect(reverse("watchlist"))


# Function for add comments
@login_required
def add_comment(request, id_listing):
    if request.method == "POST":
        form = AddComment(request.POST)
        listing = Listings.objects.get(id=id_listing)
        if form.is_valid():
            comment = Comments(id_listing=listing, id_user=request.user, text=form.cleaned_data["text"])
            comment.save()
            return HttpResponseRedirect(reverse("listings", args=[id_listing]))


# Function for add bet
@login_required
def add_bet(request, id_listing):
    if request.method == "POST":
        # Get data form
        form = SetBet(request.POST)
        # Get listing
        listing = Listings.objects.get(id=id_listing)

        if form.is_valid():
            # If there are no bets yet, then the new bet can be equal to the starting one.
            if not Bet.objects.filter(id_listing=id_listing) and form.cleaned_data["bet"] < listing.start_bid:
                messages.warning(request, "The rate must not be less than the starting price!", extra_tags="danger")
                return HttpResponseRedirect(reverse("listings", args=[id_listing]))
            # If there are already bids, then the new bid must be greater than the maximum
            if Bet.objects.filter(id_listing=id_listing) and form.cleaned_data["bet"] <= listing.max_bet:
                messages.warning(request, f"The rate must not be less than other rates! Closest value: "
                                          f"${round(listing.max_bet + 0.01, 2)}.", extra_tags="danger")
                return HttpResponseRedirect(reverse("listings", args=[id_listing]))
            # Save the bid for the current list and update the maximum bid field in the list
            new_bet = Bet(id_listing=listing, id_user=request.user, newBet=round(form.cleaned_data["bet"], 2))
            new_bet.save()
            listing.max_bet = round(form.cleaned_data["bet"], 2)
            # If the list is not tracked, then add it to the tracked list
            if len(listing.listing.filter(id_user=request.user)) == 0:
                listing.add_win_list(request.user)
            listing.save()
            return HttpResponseRedirect(reverse("listings", args=[id_listing]))

        messages.warning(request, "Wrong data!", extra_tags="danger")
        return HttpResponseRedirect(reverse("listings", args=[id_listing]))


# Function close auction
@login_required
def close_auction(request, id_listing):
    if request.method == "POST":
        get_listing = Listings.objects.get(id=id_listing)
        if Bet.objects.filter(id_listing=id_listing):
            list_bet = Bet.objects.filter(id_listing=id_listing).aggregate(Max('newBet'))
            user_win_id = Bet.objects.get(id_listing=id_listing, newBet=list_bet["newBet__max"])
            get_listing.win = User.objects.get(id=user_win_id.id_user.id)
            get_listing.open = False
            get_listing.save()

            return HttpResponseRedirect(reverse("listings", args=[id_listing]))
        get_listing.open = False
        get_listing.save()
        return HttpResponseRedirect(reverse("listings", args=[id_listing]))


# Function for winlist
@login_required
def win_list(request):
    get_win_listings = Listings.objects.filter(win=request.user)

    page_list = pag(request, get_win_listings, 3)

    active = "winlist"
    ls = [a.id_listing for a in WatchList.objects.filter(id_user=request.user)]
    return render(request, "auctions/winlist.html", {
        "page_objects": page_list[0], "count": len(WatchList.objects.filter(id_user=request.user)),
        "is_paginated": page_list[1], "next_url": page_list[3], "prev_url": page_list[2], "ls": ls,
        "active": active, "count_win": len(Listings.objects.filter(win=request.user))
    })
