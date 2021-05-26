# from Proj.CloudAppDev.server.djangoapp.restapis import get_dealer_by_id, get_dealers_from_cf
from . import restapis
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.template.loader import render_to_string

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context={}
    return render(request, 'djangoapp/about.html', context)
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    context={}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    
    if request.method == "GET":
        url = "https://ce328930.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = restapis.get_dealers_from_cf(url)
        context=dict()
        # context=dealerships
        dealer_names_json = '"}, {"full_name": "'.join([dealer.full_name for dealer in dealerships])
        dealer_names_json='{"full_name":"'+dealer_names_json+'"}'
        dealer_names_full='{"data"'+': ['+dealer_names_json+']}'

        # render_to_string('djangoapp/index.html', dealer_names_json)

        # dealer_names=', '.join([dealer.full_name for dealer in dealerships])
        # dealer_names='{"data":"'+dealer_names+'"}'
        # print(dealer_names)
        # context=dealer_names

        # json.loads(json.dumps([dict1, dict2]))
        # context= {'name': dealerships}
        # Return a list of dealer short name
        # context = json.loads(dealer_names_full)
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', dealer_names_full)



# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://ce328930.us-south.apigw.appdomain.cloud/api/review"
        # Get dealers from the URL
        #get dealers by id
        reviews= restapis.get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all dealer's short name
        # review_names = ', '.join([review.name for review in reviews])
        # Return a list of dealer short name
        return HttpResponse(reviews) 
# ...

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    review=[]
    json_payload=[]
    review["request"]=request
    review["time"] = datetime.utcnow().isoformat()
    review["dealership"] = 11
    review["review"] = "This is a great car dealer"
    json_payload["review"] = review
    url = "https://ce328930.us-south.apigw.appdomain.cloud/api/review"

    restapis.post_request(url, json_payload, dealerId=dealer_id)
# ...
def get_dealer_id(request,dealer_id):
    print(request)
    if request.method == "GET":
        url = "https://ce328930.us-south.apigw.appdomain.cloud/api/review"
        reviews = restapis.get_dealer_by_id(url,dealer_id)
        # Concat all dealer's short name
        # review_names = ', '.join([review.name for review in reviews])
        # Return a list of dealer short name
        return HttpResponse(reviews) 


