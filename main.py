import requests
import os
from unsplash.api import Api
from unsplash.auth import Auth

# Create instance of Unsplash API
unsplash_api = Api(Auth(os.getenv('UNSPLASH_ACCESS_KEY'), os.getenv('UNSPLASH_SECRET_KEY'), os.getenv('UNSPLASH_REDIRECT_URI')))

# Get access key for OpenWeatherMap API from environment variables
weather_key = os.getenv('WEATHER_KEY')

# Convert Kelvin to Fahrenheit
def from_kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

def get_search_query():
    # Create base URL for OpenWeatherMap API, hard-coding city ID for Fayetteville, AR
    url = 'http://api.openweathermap.org/data/2.5/weather?id=4110486&appid=' + weather_key

    # Get response from OpenWeatherMap API, marshal to JSON
    response = requests.get(url).json()

    # Get weather description, current temperature, and time of day
    description = response['weather'][0]['description']
    temp = int(round(from_kelvin_to_fahrenheit(response['main']['temp']), 0))
    time = 'daytime' if response['dt'] > response['sys']['sunrise'] and response['dt'] < response['sys']['sunset'] else 'nighttime'

    # Return search query
    return description + ' at ' + str(temp) + ' degrees Fahrenheit outside during the ' + time

def main():
    # Generate image url from Unsplash API
    # Not enough variation in images produced by query, so choosing random image from results
    image_url = unsplash_api.photo.random(query=get_search_query())[0].urls.raw

    # Download image
    open('image.jpg', 'wb').write(requests.get(image_url).content)

if __name__ == '__main__':
    main()