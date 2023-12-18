# Weather Wallpaper

Python script to gather weather data in Fayetteville, AR from OpenWeatherMap API and set your desktop background to a landscape photo matching the current weather from Unsplash API.<br>

Currently only configured to change the desktop background if running on Windows and MacOS. If running on Linux, the script will only download the image to the `img` directory.

## Setting up API keys
To run the Python script, you will need to have API keys for both [OpenWeatherMap](https://openweathermap.org/) as well as [Unsplash](https://unsplash.com/developers). These should be present in a `.env` at the root directory of the project, with the following format:<br>

```
# OpenWeatherMap key
WEATHER_KEY=your_key_here

# Unsplash keys
UNSPLASH_ACCESS_KEY=your_key_here
UNSPLASH_SECRET_KEY=your_key_here
UNSPLASH_REDIRECT_URI=your_key_here
```

## Installing dependencies

Before running the script, use `pip` to install the script's required dependencies found in the `requirements.txt` file:<br>

`pip install -r requirements.txt`<br>

## To run

This script can be run just once to generate a single desktop background of the weather in Fayetteville, AR at that moment:<br>

`python /path/to/main.py` or `./path/to/main.py` if the script was made executable and a shebang was added to the top of the script.<br>

The generated image will be saved to the `img` directory, the file name being the current date.<br>

### Using `cron`<br>

You can run this script using `cron` to update your desktop background periodically. Run the following command to edit your current `cron` tasks:<br>

`crontab -e`<br>

Add the following to the file to run the python script every hour:<br>

`0 * * * * /path/to/main.py`<br>

Doing this will require that the Python script is executable and includes a shebang at the beginning of the file. Run the command `which python` to get the directory in which python is installed, and add that path to a shebang at the beginning of the script:<br>

`#! /path/to/python`<br>

Run the following command to make the script executable by the user:

`chmod u+x /path/to/main.py`<br>

### Change background when weather changes

<b>Only consider the following approach if you have no API request restrictions, as it requires making calls to OpenWeatherMap API every instant to detect changes in the weather.</b><br>

You can adjust the `main` function in `main.py` to continuously check for changes in the weather and update the desktop background accordingly:<br>

```python
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

    # Get current weather and set wallpaper
    current_weather: dict = requests.get(weather_url).json()
    current_query: str = get_search_query(current_weather)
    set_wallpaper(current_query, unsplash_api)

    # Update wallpaper if change in weather and search query is detected
    while True:
        new_weather: dict = requests.get(weather_url).json()
        new_query: str = get_search_query(new_weather)
        if new_query != current_query:
            set_wallpaper(new_query, unsplash_api)
            current_query = new_query
        time.sleep(1)
```

Because the loop is infinite, it's recommended to run the script in the background using `nohup`:<br>

`nohup /path/to/main.py &`<br>

To stop the process, run the following command in the terminal to find the process ID:<br>

`ps ax | grep main.py`<br>

The ID of a process is denoted by the number found at the beginning of a new line output by the command. Then, use the `kill` command to stop the process, replacing `id` with the number you found previously:<br>

`kill id`<br>
