import requests
import json
from auth import DADATA_TOKEN, OPENWEATHER_TOKEN    # import api tokens

weather_url = 'http://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/country'
weather_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Token {DADATA_TOKEN}'
}


def weather_response(city, w_token=OPENWEATHER_TOKEN):
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={w_token}&units=metric')
    return response.json()


def country_response(country='RU'):
    response = requests.post(url=weather_url,
                             headers=weather_headers,
                             data=json.dumps({'query': f'{country}'}))
    return response.json()['suggestions'][0]['data']['name_short']

