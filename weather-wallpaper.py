"""
Author: Cade DuPont
Date: 05/23/23
Description: Gather weather data from Fayetteville, AR and set
            the desktop wallpaper to a random image from Unsplash
            based on a generated search query.
"""

import requests, os, platform, datetime, dotenv
from unsplash.api import Api
from unsplash.auth import Auth

# Import OS specific modules for changing desktop wallpaper
if platform.system() == 'Windows':
    import ctypes
elif platform.system() == 'Darwin':
    from appscript import app, mactypes

def get_search_query(weather: dict) -> str:
    # Get weather description and temperature converted from Kelvin to Fahrenheit
    description: str = weather['weather'][0]['description']

    month: str = datetime.datetime.fromtimestamp(weather['dt']).strftime('%B')
    if month in ['December', 'January', 'February']:
        season: str = 'winter'
    elif month in ['March', 'April', 'May']:
        season: str = 'spring'
    elif month in ['June', 'July', 'August']:
        season: str = 'summer'
    else:
        season: str = 'fall'

    # Get time of day based on whether current time is between sunrise and sunset, set season based on month weather data was gathered
    time: str = 'day' if weather['dt'] > weather['sys']['sunrise'] and weather['dt'] < weather['sys']['sunset'] else 'night'
    
    # Return search query based on given description, temperature, and time of day
    return f'{description} landscape during a {season} {time} desktop wallpaper'

def set_wallpaper(query: str, unsplash: Api) -> None:
    # Set file path and get URL for image based on search query
    filepath: str = os.path.abspath(f'{str(datetime.date.today())}.jpg')
    url: str = unsplash.photo.random(query=query, orientation='landscape')[0].urls.raw

    # Write contents of URL to file with the name of the current date
    open(filepath, 'wb').write(requests.get(url).content)

    # Set desktop wallpaper based on OS
    if platform.system() == 'Windows':
        ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 0)
    elif platform.system() == 'Darwin':
        app('Finder').desktop_picture.set(mactypes.File(filepath))

def main() -> None:
    # Load environment variables
    dotenv.load_dotenv()

    # Create Unsplash API instance
    unsplash_auth: Auth = Auth(os.getenv('UNSPLASH_ACCESS_KEY'),
                               os.getenv('UNSPLASH_SECRET_KEY'),
                               os.getenv('UNSPLASH_REDIRECT_URI'))
    unsplash_api: Api = Api(unsplash_auth)

    # Create URL for current weather data
    weather_url: str = f'http://api.openweathermap.org/data/2.5/weather?id=4110486&appid={os.getenv("WEATHER_KEY")}'

    # Get search query based on current weather data and set desktop wallpaper
    query: str = get_search_query(requests.get(weather_url).json())
    set_wallpaper(query, unsplash_api)

if __name__ == '__main__':
    main()