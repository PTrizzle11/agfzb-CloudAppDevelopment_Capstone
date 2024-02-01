from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import get_request, get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
# Create an `about` view to render a static about page
def about(request):
    context={}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context={}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context={}
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Logout the user '{}'".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context={}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context={}
        url = "https://patrickjodon-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Add to context
        context["dealerships"] = dealerships
        # rendering page
        return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, dealerId):
    if request.method == "GET":
        context={}
        url = "https://patrickjodon-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        #Getting reivews from the url and dealerid
        reviews = get_dealer_reviews_from_cf(url, dealerId)
        #add reviews to context
        context["reviews"] = reviews
        context["dealer_id"] = dealerId
        #Returning render
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    #Checking if user is authenticated
    if request.user.is_authenticated:
        if request.method == "GET":
            #If get is selected, query cars by dealer and render the html
            context={}
            url = "https://patrickjodon-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
            dealer_name = ""
            dealerships = get_dealers_from_cf(url)
            for dealer in dealerships:
                if dealer.id == dealer_id:
                    dealer_name = dealer.full_name
            cars = CarModel.objects.filter(dealerid=dealer_id)
            context["cars"] = cars
            context["dealer_id"] = dealer_id
            context["dealer_name"] = dealer_name
            return render(request, 'djangoapp/add_review.html', context)
        elif request.method == "POST":
            url = "https://patrickjodon-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
            review = {}
            review["id"] = 123
            review["time"] = datetime.utcnow().isoformat()
            review["name"] = "Patrick ODonnell"
            review["dealership"] = dealer_id
            review["review"] = "Bad Cars!"
            review["purchase"] = True
            review["purchase_date"] = "1/1/2024"
            review["car_make"] = "Jeep"
            review["car_model"] = "SUV"
            review["car_year"] = 2024
            #Creating payload
            json_payload = {}
            json_payload["review"] = review
            #sending review
            response = post_request(url, json_payload, dealerId=dealer_id)
            review_response = response
            return HttpResponse(review_response)
    else:
        return HttpResponse('not authenticated')