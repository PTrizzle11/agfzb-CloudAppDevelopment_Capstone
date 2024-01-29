import requests
import json
import time
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        api_key=kwargs["api_key"]
    except:
        api_key = None
    if api_key:
        try:    
            authenticator = IAMAuthenticator(api_key)
            natural_language_understanding = NaturalLanguageUnderstandingV1(
            version=kwargs["params"]["version"],
            authenticator=authenticator)
            natural_language_understanding.set_service_url(url)
            response = natural_language_understanding.analyze(
                text=kwargs["params"]["text"],
                return_analyzed_text=kwargs["params"]["return_analyzed_text"],
                language="en",
                features=Features(
                    entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
                    keywords=KeywordsOptions(emotion=True, sentiment=True, limit=2))
            ).get_result()
            sentiment = response["keywords"][0]["sentiment"]["label"]
            return sentiment
        except ApiException as ex:
            # If any error occurs
            print("Network exception occurred: " + ex.message)
    else:
        try:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
        except:
            # If any error occurs
            print("Network exception occurred")
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content 
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            results.append(dealer_obj)

    return results

def get_dealerships_by_id(url, **kwargs):
    results = []
    json_result = get_request(url, id = id)
    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, id=dealerId)
    if json_result:
        reviews = json_result
        for review in reviews:
            review_doc = review
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
            purchase_date=review_doc["purchase_date"], review=review_doc["review"], car_make=review_doc["car_make"],
            car_model=review_doc["car_model"], car_year=review_doc["car_year"], sentiment=analyze_review_sentiments(review_doc["review"]),
            id=review_doc["id"])
            results.append(review_obj)
    return results

def analyze_review_sentiments(text):
    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/bdbd65e6-2492-45c2-afb9-a8a91488bbec"
    api_key = "8OXk7m1vfIvTsWRlmDZO5bNgHjZzLMRFckDrkG74thKs"
    params = dict()
    params["text"] = text
    params["version"] = "2022-04-07"
    params["features"] = ["sentiment"]
    params["return_analyzed_text"] = False
    response = get_request(url, params = params, api_key = api_key)
    print(response)
    return response
    