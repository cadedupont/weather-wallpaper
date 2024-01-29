# Weather Wallpaper

This Python script fetches weather data for Fayetteville, AR from the OpenWeatherMap API and sets your desktop background to a corresponding landscape photo from the Unsplash API.

Currently only configured to change the desktop background for Windows and macOS systems. On Linux systems, the script will only download the image to the root directory of the project.

## How to Use
To run the application on your machine, you'll first need to either clone this repository or download the source code as a ZIP file. Then, follow the steps below to set up the application.

Run the following command in your machine's terminal to clone the repository:

```bash
$ git clone https://github.com/cadedupont/weather-wallpaper.git
```

If you chose to download the source code as a ZIP file, extract the ZIP file to a directory of your choice.

Then, navigate to the project's root directory:
```bash
$ cd /path/to/weather-wallpaper
```

## Setting up API keys
Before running the script, obtain API keys for [OpenWeatherMap](https://openweathermap.org/) and [Unsplash](https://unsplash.com/developers). Included in the project is a `.env.example` file formatted as follows:

```bash
# OpenWeatherMap key
WEATHER_KEY='your_key_here'

# Unsplash keys
UNSPLASH_ACCESS_KEY='your_key_here'
UNSPLASH_SECRET_KEY='your_key_here'
UNSPLASH_REDIRECT_URI='your_key_here'
```

Rename the file to `.env` and replace each instance of `your_key_here` with your corresponding API key.

## Installing Dependencies
Ensure you have the required dependencies by running:

```bash
$ pip install -r requirements.txt
```

## Running the Script

### One-time Execution
Execute the script to generate a single desktop background reflecting the current weather:

```bash
$ python /path/to/weather-wallpaper.py
```

If you have a shebang at the beginning of the script, you can run it directly:
```bash
$ ./path/to/weather-wallpaper.py
```

The generated file will be saved in the root directory of the project, the name of the file being the current date formatted as `YYYY-MM-DD.jpg`.

### Using `cron` for Periodic Updates
Edit your `cron` tasks to run the script periodically. Open the `cron` configuration:

```bash
$ crontab -e
```

Add the following line to run the script every hour:

```bash
$ 0 * * * * /path/to/weather-wallpaper.py
```

Ensure the script is executable and has a shebang at the beginning.

```bash
$ chmod u+x /path/to/weather-wallpaper.py
```

### Continuous Background Updates
**Note:** This approach continuously checks for weather changes, making frequent OpenWeatherMap API calls. Use it only if there are no API request restrictions.

Adjust the `main` function in `weather-wallpaper.py` to continuously update the desktop background based on weather changes:

```python
# ... (previous code)

while True:
    new_weather: dict = requests.get(weather_url).json()
    new_query: str = get_search_query(new_weather)
    if new_query != current_query:
        set_wallpaper(new_query, unsplash_api)
        current_query = new_query
    time.sleep(1)
```

Run the script in the background using `nohup`:

```bash
$ nohup /path/to/weather-wallpaper.py &
```

To stop the process, find the process ID:

```bash
$ ps ax | grep weather-wallpaper.py
```

Use the `kill` command to stop the process:

```bash
$ kill id
```

## License

This project is licensed under the [MIT License](LICENSE).