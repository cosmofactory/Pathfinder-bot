import requests
import os


from dotenv import load_dotenv


load_dotenv()
MAX_RESPONSE_RESULTS = 5


API_KEY = (('key'), (os.getenv('API_KEY')))

def get_api_answer(radius, location, type):
    """Requests information from google servers.
    
    The function does the following:
    - receives a json from google
    - checks if business is operational and has ratings
    - returns top 5 places sorted by rating.
    """

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    payload = (API_KEY, radius, location, type)
    headers = {}

    response = requests.request("GET", url, headers=headers, params=payload)

    response = response.json().get('results')
    filtered_response = []
    for obj in response:  # Removing closed and no-rating places
        try:
            if obj['business_status'] == 'OPERATIONAL' and obj['rating']:
                filtered_response.append(obj)
        except Exception:
            pass
    return sorted(
        filtered_response,
        key=lambda x: x['rating'],
        reverse=True
    )[:MAX_RESPONSE_RESULTS]


def parse_answer(sorted_response, number):
    expected_information = (
        'name',
        'rating',
        'vicinity',
        'price_level',
    )
    expected_return = []
    for i in expected_information:
        try:
            expected_return.append(sorted_response[number][i])
        except Exception:
            expected_return.append('Нет данных')
    return expected_return


def send_message(number, sorted_response):
    name, rating, address, price_level, types = parse_answer(sorted_response, number)
    return(   f'Название: {name}\n'
            f'Рейтинг: {rating}\n'
            f'Адрес: {address}\n'
            f'Ценовой диапазон: {price_level}\n'
            )
