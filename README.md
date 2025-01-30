# Atmosonic - *Your* Personal Weather: <a href="atmosonic.streamlit.app">atmosonic.streamlit.app</a>
## Powered By: 
<pre><a href="https://streamlit.io"><img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-lighttext.png" width=150></a></pre>

If you get an error, please wait ~30 seconds, as the API most likely rate limited

## How it works:
This is a Python-based application designed with and hosted on Streamlit. It uses many of Streamlit's built-in widgets, as well as some HTML with Streamlit markdowns to create custom text areas.
- Gets the user's current location (usually ends up somewhere in Oregon since its hosted on Streamlit
- Uses the free Open Meteo API to get current (15 minute) weather conditions, daily high/low, and hourly conditions to compare change in the past hour
- Displays the weather with an icon and description
- Added touch: Plays music that corresponds to the weather. If there's an error, the fallback is 24D Skyfall by Adele.

## Want to use it locally?
- A: Download the app through your browser
- B: Clone this repo and change the place parameter to your location for permanent location
