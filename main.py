import requests
import os
from unsplash.api import Api
from unsplash.auth import Auth

# Get access key, secret key adn redirect uri from environment variables for unsplash access
unsplash_access = os.getenv('UNSPLASH_ACCESS_KEY')
unsplash_secret = os.getenv('UNSPLASH_SECRET_KEY')
unsplash_uri = os.getenv('UNSPLASH_REDIRECT_URI')

# Create an instance of the Auth and Api classes
unsplash_api = Api(Auth(unsplash_access, unsplash_secret, unsplash_uri))

# Get access key for OpenWeatherMap from environment variables
weather_key = os.getenv('WEATHER_KEY')

# Convert Kelvin to Fahrenheit
def from_kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

# Get weather description and temperature from OpenWeatherMap API
def get_weather_desc():
    url = 'http://api.openweathermap.org/data/2.5/weather?id=4110486&appid=' + weather_key
    response = requests.get(url).json()
    return response['weather'][0]['description'] + ' and ' + str(round(from_kelvin_to_fahrenheit(response['main']['temp']), 2)) + ' degrees Fahrenheit'

def main():
    # Generate image url from Unsplash API
    image_url = unsplash_api.search.photos(get_weather_desc(), page=1, per_page=1)['results'][0].urls.raw

    # Download image
    open('image.jpg', 'wb').write(requests.get(image_url).content)

if __name__ == '__main__':
    main()