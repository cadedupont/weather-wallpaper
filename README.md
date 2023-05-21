# weather-photo-frame
Python script for gathering weather data from OpenWeatherMap API, using as a search query to download an image from Unsplash to set as desktop wallpaper.<br>

Currently has limited functionality. Requires installing various dependencies, adding private API keys to the system's environment variables, and is only configured to change the desktop wallpaper of MacOS devices.<br>

When a change in weather is detected, a new image will be downloaded and set as the desktop background. A timestamp will be printed to the `output.log` file.<br>

## To run
Because the script uses an infinite loop to detect changes in the weather, the script must run in the background. This can be done using `nohup`:<br>

`nohup /path/to/main.py &`<br>

To stop the process, run the following command in the terminal to find the process ID:<br>

`ps ax | grep main.py`<br>

The ID of a process is denoted by the number found at the beginning of a new line output by the command. Then, use the `kill` command to stop the process, replacing `id` with the number you found previously:<br>

`kill id`<br>