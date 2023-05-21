#! /opt/homebrew/bin/python3

import requests
import os
from datetime import datetime
from appscript import app, mactypes
from unsplash.api import Api
from unsplash.auth import Auth

# Create instance of Unsplash API, get URL for current weather
unsplash_api = Api(Auth(os.getenv('UNSPLASH_ACCESS_KEY'), os.getenv('UNSPLASH_SECRET_KEY'), os.getenv('UNSPLASH_REDIRECT_URI')))
weather_url = f'http://api.openweathermap.org/data/2.5/weather?id=4110486&appid={os.getenv("WEATHER_KEY")}'

# Convert Kelvin to Fahrenheit
def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

# Get search query for Unsplash API
def get_search_query(weather):
    # Get weather description and temperature as an integer
    description = weather['weather'][0]['description']
    temp = int(round(kelvin_to_fahrenheit(weather['main']['temp']), 0))

    # Based on temperature, get temperature description
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

    # Get time of day description based on whether current time is between sunrise and sunset
    time = 'day' if weather['dt'] > weather['sys']['sunrise'] and weather['dt'] < weather['sys']['sunset'] else 'night'

    # Return search query
    return description + ' and ' + temp_desc + ' weather outside during the ' + time + ' landscape'

# Return image URL from Unsplash API
def get_image_url(weather):
    return unsplash_api.photo.random(query=get_search_query(weather), orientation='landscape')[0].urls.raw

# Get current weather
def get_weather():
    return requests.get(weather_url).json()

# Download image from Unsplash API and set as wallpaper
def set_wallpaper(url):
    open('image.jpg', 'wb').write(requests.get(url).content)
    app('Finder').desktop_picture.set(mactypes.File(os.getcwd() + '/image.jpg'))

def main():
    # Get current weather and set wallpaper
    curr_weather = get_weather()
    set_wallpaper(get_image_url(curr_weather))

    # Continue checking for new weather, if new weather is different, set new wallpaper
    while True:
        new_weather = get_weather()
        if get_search_query(new_weather) != get_search_query(curr_weather):
            set_wallpaper(get_image_url(new_weather))
            curr_weather = new_weather

# If this file is run directly, call main function
if __name__ == '__main__':
    main()