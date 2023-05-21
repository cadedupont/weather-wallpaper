import requests
import os
from unsplash.api import Api
from unsplash.auth import Auth

# Create instance of Unsplash API, get OpenWeatherMap API key from environment variables
unsplash = Api(Auth(os.getenv('UNSPLASH_ACCESS_KEY'), os.getenv('UNSPLASH_SECRET_KEY'), os.getenv('UNSPLASH_REDIRECT_URI')))
WEATHER_KEY = os.getenv('WEATHER_KEY')

# Convert Kelvin to Fahrenheit
def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

def get_search_query(weather):
    # Get weather description, current temperature
    description = weather['weather'][0]['description']
    temp = int(round(kelvin_to_fahrenheit(weather['main']['temp']), 0))
    
    # Get temperature description
    if temp < 32:
        temp_desc = 'freezing'
    elif temp < 50:
        temp_desc = 'cold'
    elif temp < 70:
        temp_desc = 'cool'
    elif temp < 80:
        temp_desc = 'warm'
    else:
        temp_desc = 'hot'

    # Get time of day
    time = 'day' if weather['dt'] > weather['sys']['sunrise'] and weather['dt'] < weather['sys']['sunset'] else 'night'

    # Return search query
    return description + ' and ' + temp_desc + ' outside during the ' + time

def main():
    # Get weather from OpenWeatherMap API, marshal to JSON
    url = f'http://api.openweathermap.org/data/2.5/weather?id=4110486&appid={WEATHER_KEY}'
    curr_weather = requests.get(url).json()

    # Get image url from Unsplash API and download to file
    image_url = unsplash.photo.random(query=get_search_query(curr_weather))[0].urls.raw
    open('image.jpg', 'wb').write(requests.get(image_url).content)

    # Update image if new weather is different from old weather
    while True:
        new_weather = requests.get(url).json()
        if get_search_query(new_weather) != get_search_query(curr_weather):
            image_url = unsplash.photo.random(query=get_search_query(new_weather))[0].urls.raw
            open('image.jpg', 'wb').write(requests.get(image_url).content)
            curr_weather = new_weather

if __name__ == '__main__':
    main()