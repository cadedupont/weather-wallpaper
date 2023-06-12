"""
Author: Cade DuPont
Date: 05/23/23
Description: This script gathers weather data from Fayetteville, AR and sets
            the desktop wallpaper to a random image from Unsplash based on
            a generated search query.
"""

# Import modules
import requests, os
from unsplash.api import Api
from unsplash.auth import Auth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    return description + ' landscape with ' + temp_desc + ' weather during the ' + time + ' time'

# Get current weather
def get_weather():
    return requests.get(weather_url).json()

# Download image from Unsplash API and set as wallpaper
def set_wallpaper(weather):
    # Write contents of URL to image.jpg
    url = unsplash_api.photo.random(query=get_search_query(weather), orientation='landscape')[0].urls.raw
    open('image.jpg', 'wb').write(requests.get(url).content)

    # Set wallpaper according to OS
    if os.name == 'nt':
        import ctypes
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.getcwd() + '/image.jpg', 0)
    elif os.name == 'posix':
        from appscript import app, mactypes
        app('Finder').desktop_picture.set(mactypes.File(os.getcwd() + '/image.jpg'))

def main():
    # Get current weather and set wallpaper
    set_wallpaper(get_weather())

# If this file is run directly, call main function
if __name__ == '__main__':
    main()