import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url,  headers={'Content-Type': 'application/json'},  params=kwargs)
        # Call get method of requests library with URL and parameters
        # if api_key:
        #     response = requests.get(url,headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key), params=kwargs)
        # else:
        #     response = requests.get(url,  headers={'Content-Type': 'application/json'},  params=kwargs)
        print(response)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except:
        # If any error occurs
        print("Network exception occurred")
    return json_data


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    params=dealerreview
    # params = dict()
    # params["text"] = kwargs["text"]
    # params["version"] = kwargs["version"]
    # params["features"] = kwargs["features"]
    # params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    response = requests.get("https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/daa0c140-e05d-470e-9580-db100c12b5e0",
                             params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', ""))
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    # print(json_result)
    # print ('ok ')
    # print(json_result["data"][0]["dealerships"])
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["data"][0]["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results   


def get_dealer_reviews_from_cf(url, dealerId, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["data"][0]["reviews"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            review_obj = DealerReview(car_make=review_doc["car_make"], car_model=review_doc["car_model"], car_year=review_doc["car_year"], dealership=review_doc["dealership"],
                                   id=review_doc["id"],  name=review_doc["name"], purchase=review_doc["purchase"], purchase_date=review_doc["purchase_date"], review=review_doc["review"])
            reviewid=review_obj.id
            
            # print(review_obj.id)
            # print(dealerid)
            if(reviewid==dealerId):
                results.append(review_obj)
                # review_obj.sentiment = analyze_review_sentiments(review_obj.review)
                # results.append(review_obj.sentiment)

    return results  


def get_dealer_by_id(url, dealerId, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["data"][0]["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            dealerid=dealer_obj.id
            # print(dealer_obj.id)
            # print(dealerid)
            if(dealerid==dealerId):
                results.append(dealer_obj)

    return results 

# def get_dealers_by_state(url, state, **kwargs):
#     results = []
#     # Call get_request with a URL parameter
#     json_result = get_request(url, state=state)
#     if json_result:
#         # Get the row list in JSON as dealers
#         states = json_result["data"][0]["dealerships"]
#         # For each dealer object
#         for state in states:
#             # Get its content in `doc` object
#             dealer_doc = state["doc"]
#             # Create a CarDealer object with values in `doc` object
#             dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
#                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
#                                    short_name=dealer_doc["short_name"],
#                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
#             results.append(dealer_obj)

#     return results 

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    requests.post(url, params=kwargs, json=json_payload)
# e.g., response = requests.post(url, params=kwargs, json=payload)


# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative