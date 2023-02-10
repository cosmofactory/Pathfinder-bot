import requests
from pprint import pprint


def get_api_answer(radius, location, type):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

    API_KEY = (('key'), ('AIzaSyAjBPpupkZT0Ivvc-FiyQpAhHEhEvwEE2c'))
    payload = (API_KEY, radius, location, type)
    headers = {}

    response = requests.request("GET", url, headers=headers, params=payload)

    response = response.json().get('results')
    sorted_response = sorted(response, key=lambda x: x['rating'], reverse=True)
    pprint(sorted_response)
    
    for i in sorted_response:
        pprint(i['rating'])



radius = (('radius'), (1000))
location = (('location'), ('59.861304,30.322210'))
type = (('type'), ('restaurant'))
get_api_answer(radius, location, type)
