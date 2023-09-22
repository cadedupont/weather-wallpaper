# Weather Wallpaper

Python script for gathering current weather data from OpenWeatherMap API into a search query for Unsplash, downloading the image and setting it as the desktop wallpaper.<br>

Currently only configured to change the desktop wallpaper for MacOS and Windows devices, and is hard-coded to gather weather data from Fayetteville, AR.<br>

## Setting up API keys<br>
To run the Python script, you will need to have API keys for both [OpenWeatherMap](https://openweathermap.org/) as well as [Unsplash](https://unsplash.com/developers). These should be present in a `.env` file in the `src` directory of the project, with the following format:<br>

```
# OpenWeatherMap key
WEATHER_KEY=your_key_here

# Unsplash access key
UNSPLASH_ACCESS_KEY=your_key_here

# Unsplash secret key
UNSPLASH_SECRET_KEY=your_key_here

# Unsplash redirect uri
UNSPLASH_REDIRECT_URI=your_key_here
```

## To run<br>

### Installing dependencies<br>

Before running the script, use `pip` to install the script's required dependencies found in the `requirements.txt` file:<br>

`pip install -r requirements.txt`<br>

---

### Using `cron`<br>

You can run this script using `cron` to update your desktop background periodically. Run the following command to edit your current `cron` tasks:<br>

`crontab -e`<br>

Add the following to the file to run the python script every hour:<br>

`0 * * * * /path/to/main.py`<br>

Doing this will require that the Python script is executable and includes a shebang at the beginning of the file. Run the command `which python` to get the directory in which python is installed, and add that path to a shebang at the beginning of the script:<br>

`#! /path/to/python`<br>

Run the following command to make the script executable by the user:

`chmod u+x /path/to/main.py`<br>

---

### Other run options<br>

This script can be run just once to generate a single desktop background of the weather in Fayetteville, AR at that moment:<br>

`python /path/to/main.py` or `./path/to/main.py` if the script was made executable.<br>

<b>Only consider the following approach if you have no API request restrictions, as it requires making calls to OpenWeatherMap API every instant to detect changes in the weather</b><br>

You can add a loop to the `main` function in the script to update the desktop background when a change in search query is detected:<br>

```py
def main():
    # Get current weather and set wallpaper
    curr_weather = get_weather()
    set_wallpaper(curr_weather)

    # Continue checking for new weather, if new weather is different, set new wallpaper
    while True:
        new_weather = get_weather()
        if get_search_query(new_weather) != get_search_query(curr_weather):
            set_wallpaper(new_weather)
            curr_weather = new_weather
```

Because the loop is infinite, it's recommended to run the script in the background using `nohup`:<br>

`nohup /path/to/main.py &`<br>

To stop the process, run the following command in the terminal to find the process ID:<br>

`ps ax | grep main.py`<br>

The ID of a process is denoted by the number found at the beginning of a new line output by the command. Then, use the `kill` command to stop the process, replacing `id` with the number you found previously:<br>

`kill id`<br>
