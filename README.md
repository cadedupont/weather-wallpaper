# weather-photo-frame
Python script for gathering weather data from OpenWeatherMap API, using as a search query to download an image from Unsplash to set as desktop wallpaper.<br>

Currently has limited functionality. Requires installing various dependencies, adding private API keys to the system's environment variables, and is only configured to change the desktop wallpaper of MacOS devices.

## To run
Because the script uses an infinite loop to detect changes in the weather, the script must run in the background. This can be done using `nohup`:<br>

`nohup /path/to/main.py > output.log &`<br>

This will run the Python script in the background, piping what's printed by the script to the `output.log` file.<br>

To stop the process, run the following command in the terminal to find the process ID:<br>

`ps ax | grep main.py`<br>

The ID of a process is denoted by the 5-digit number found at the beginning of a new line output by the command. Then, use the `kill` command to stop the process:<br>

`kill id`<br>

Replace 'id' with the 5-digit number found previously.