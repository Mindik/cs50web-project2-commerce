# Project 2
CS50’s Web Programming with Python and JavaScript
---

Project completed in [CS50W](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript) course.

The project was implemented in [PyCharm](https://www.jetbrains.com/pycharm/) 2020.1.2 (Professional Edition).
Applied technology [Django](https://www.djangoproject.com/), [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5), [CSS3](https://www.w3schools.com/css/) ([SASS](https://sass-lang.com/)).

The task can be viewed at the link - [Project 2: Commerce](https://cs50.harvard.edu/web/2020/projects/2/commerce/).

>"Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, 
>comment on those listings, and add listings to a “watchlist.”"


## Project structure

1. [auctions](auctions)

    Auctions Application Folder

    * [static](auctions/static/auctions)
 
         Contains images and CSS files
             
        * [styles.scss](auctions/static/auctions/styles.scss)
     
             SASS file containing CSS markup for all pages of the application.
        
    * [templates](auctions/templates/auctions)
    
    Page Templates
    
    * [urls.py](auctions/urls.py)
    
    File url for Encyclopedia Application
    
    * [views.py](auctions/views.py)
    
    A view function, or view for short, is a Python function that takes a Web request and returns a Web response.
    
    * [models.py](auctions/views.py)
    
    View file for database records.
     
2. [manage.py](manage.py)

    Main file Django
    
    
## App appearance

#### Admin

![Admin](https://i.ibb.co/txPdkz2/admin2.jpg)

![Admin](https://i.ibb.co/h2tXGLs/admin3.jpg)

The administrator can view, edit, delete and create any records.

#### Model

![Model](https://i.ibb.co/DDp5Rp9/admin1.jpg)

Added new data models.

#### Main page

![Main page](https://i.ibb.co/1bBy840/main1.jpg)

![Main page](https://i.ibb.co/Wspntn7/main2.jpg)

The main page displays a list of all open auctions, divided into pages. Each auction shows the author, 
title, short text, starting price, image, categories and creation date.

#### Create Page

![Create Page](https://i.ibb.co/dfsYw7m/create.jpg)

Registered users can go to the page for creating a new auction. 
Title, description and starting price are required! Image categories and address - no.

#### Listing Page

![Listing](https://i.ibb.co/hgTfPh3/list1.jpg)

The auction page allows the author to close it and designate a winner if bids have been made. 
Other users can place bids on the page.

![Listing](https://i.ibb.co/7YP2HrQ/bet1.jpg)

If there are no bets yet, then the new bet must be at least equal to the starting one. 
If this is not the case, we will receive an error message.

![Listing](https://i.ibb.co/TTMtp7r/bet2.jpg)

If there are rates, then the new rate must be greater than the maximum. Otherwise, we will get an error.

![Listing](https://i.ibb.co/LgVDvFY/list2.jpg)

All registered users can leave comments.

![Listing](https://i.ibb.co/GQSf1sq/bet3.jpg)

![Listing](https://i.ibb.co/f95qDrF/bet4.jpg)

The author of the auction can close it, and the winner will receive a notification and an icon for the number of auctions won.

Creating an auction and adding a bid will automatically add the auction to the watched list.

#### Categories List

![Categories](https://i.ibb.co/ckPXxFn/cat1.jpg)

The Category List page displays a list of all categories and the number of unclosed auctions in each category.

#### Category

![Category](https://i.ibb.co/4sMnzrm/cat2.jpg)

You can see a list of auctions in this category.

#### Watchlist

![Watchlist](https://i.ibb.co/3dVwvF9/watch.jpg)

The watchlist shows all monitored auctions, even after they have closed..
