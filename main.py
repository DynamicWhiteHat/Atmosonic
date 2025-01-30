import time
import streamlit as st
import requests
from geopy.geocoders import Nominatim
import json
import geocoder
from datetime import datetime
import random

#configuring the page
st.set_page_config(
   page_title="Atmosonic - Your Weather App",
   page_icon="🌡️",
   layout="wide",
   initial_sidebar_state="expanded",
)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&family=Open+Sans:ital,wght@0,300..800;1,300..800&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&family=Source+Sans+3:ital,wght@0,200..900;1,200..900&display=swap');
        .text, .text1 {
            text-align: center;
            color: #FFFFFF;
            font-family: 'Roboto', sans-serif;
            font-size: 1.5em;
            font-weight: 500;
        }
        .text1 {
            font-size: 1.1em;
            }
        .highlight-text {
            color: #ff4b4b;
            display: inline;
            font-weight: bold;
        }
        .holder {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-top: 2em;
            margin-bottom: 1em;
        }
    </style>
""", unsafe_allow_html=True)

#Title
st.title (':red[Atmosonic: Your Weather App]')

# API & Location

weather_phrases = {
    0: "Go outside! It's sunny!",
    1: "A beautiful day ahead, mostly clear skies!",
    2: "Enjoy the day with a few clouds in the sky!",
    3: "The sky is fully covered in clouds, but no rain for now.",
    45: "It's foggy out there, be cautious while driving.",
    48: "Dense fog with ice deposits, make sure to stay safe.",
    51: "A light drizzle is falling, grab an umbrella!",
    53: "It’s drizzling moderately, a perfect day for a cozy inside time.",
    55: "Heavy drizzle, best to stay dry indoors!",
    56: "Light freezing drizzle, slippery roads ahead, be careful!",
    57: "Dense freezing drizzle, making the ground icy—stay safe!",
    61: "A slight rain is falling, a light jacket should do.",
    63: "It's raining moderately, don’t forget your umbrella!",
    65: "Heavy rain is pouring down, best to stay inside!",
    66: "Light freezing rain, roads are getting slick, drive cautiously.",
    67: "Heavy freezing rain, dangerous conditions—stay indoors if possible.",
    71: "A light snowfall is falling, perfect for a winter walk!",
    73: "Moderate snow is falling, time to bundle up!",
    75: "Heavy snow is falling, visibility is low—stay warm and safe!",
    77: "Snow grains are drifting through the air—light and cold!",
    80: "A few light rain showers, but it won't last long.",
    81: "Moderate rain showers are expected, grab your raincoat!",
    82: "Heavy rain showers are coming your way, stay indoors if you can!",
    85: "A few light snow showers, a wintery sight but not much accumulation.",
    86: "Heavy snow showers are coming, the roads will be covered quickly!",
    95: "A thunderstorm is rolling in, best to stay indoors.",
    96: "Thunderstorm with slight hail, be careful outside.",
    99: "A severe thunderstorm with heavy hail is here, stay safe and indoors!"
}



weather_codes = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Fime Fog",
    51: "Drizzle: Light intensity",
    53: "Drizzle: Moderate intensity",
    55: "Drizzle: Dense intensity",
    56: "Freezing Drizzle: Light intensity",
    57: "Freezing Drizzle: Dense intensity",
    61: "Rain: Slight intensity",
    63: "Rain: Moderate intensity",
    65: "Rain: Heavy intensity",
    66: "Freezing Rain: Light intensity",
    67: "Freezing Rain: Heavy intensity",
    71: "Snow fall: Slight intensity",
    73: "Snow fall: Moderate intensity",
    75: "Snow fall: Heavy intensity",
    77: "Snow grains",
    80: "Rain showers: Slight intensity",
    81: "Rain showers: Moderate intensity",
    82: "Rain showers: Violent intensity",
    85: "Snow showers: Slight intensity",
    86: "Snow showers: Heavy intensity",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

weather_music = {
    # Rainy Weather 🌧️ (codes for rain, drizzle, and rain showers)
    (51, 53, 55, 61, 63, 65, 80, 81, 82): [
        "Rainy Days and Mondays – The Carpenters",
        "Purple Rain – Prince",
        "Set Fire to the Rain – Adele",
        "No Rain – Blind Melon",
        "Riders on the Storm – The Doors"
    ],
    
    # Sunny Weather ☀️ (clear sky or mostly clear)
    (0, 1): [
        "Walking on Sunshine – Katrina and the Waves",
        "Here Comes the Sun – The Beatles",
        "Good Vibrations – The Beach Boys",
        "Pocketful of Sunshine – Natasha Bedingfield",
        "Sun is Shining – Bob Marley"
    ],
    
    # Cloudy Weather ☁️ (partly cloudy, mostly cloudy, overcast)
    (2, 3, 45, 48): [
        "Cloudy – Simon & Garfunkel",
        "Both Sides, Now – Joni Mitchell",
        "Just Like Heaven – The Cure",
        "Cloudbusting – Kate Bush",
        "A Hazy Shade of Winter – Simon & Garfunkel"
    ],
    
    # Snowy Weather ❄️ (snowfall, snow grains)
    (71, 73, 75, 77, 85, 86): [
        "Let It Snow! Let It Snow! Let It Snow! – Dean Martin",
        "White Winter Hymnal – Fleet Foxes",
        "Sweater Weather – The Neighbourhood",
        "Coldplay – Snow Patrol",
        "Do You Want to Build a Snowman? – Kristen Bell, Agatha Lee Monn"
    ],
    
    # Thunderstorm Weather 🌩️ (thunderstorm, thunderstorm with hail)
    (95, 96, 99): [
        "Thunderstruck – AC/DC",
        "Lightning Crashes – Live",
        "Blinding Lights – The Weeknd",
        "Electric Feel – MGMT",
        "Bohemian Rhapsody – Queen"
    ],
    
    # Windy Weather 🌬️ (strong winds)
    (71, 73, 75, 77): [
        "Blowin' in the Wind – Bob Dylan",
        "Dust in the Wind – Kansas",
        "Wild Is the Wind – Nina Simone or David Bowie",
        "Against the Wind – Bob Seger",
        "Candle in the Wind – Elton John"
    ],
    
    # After the Storm (Hopeful Weather) 🌈
    (0, 1, 3, 5): [
        "Rainbow – Kacey Musgraves",
        "Somewhere Over the Rainbow – Israel Kamakawiwo'ole",
        "I Can See Clearly Now – Johnny Nash",
        "Here Comes the Sun – The Beatles",
        "Walking on Sunshine – Katrina and the Waves"
    ]
}


def get_wind_condition(wind_speed):
    if wind_speed >= 0 and wind_speed <= 5:
        return "Light breeze"
    elif wind_speed > 5 and wind_speed <= 10:
        return "Breezy"
    elif wind_speed > 10 and wind_speed <= 20:
        return "Moderate wind"
    elif wind_speed > 20 and wind_speed <= 30:
        return "Strong wind"
    elif wind_speed > 30 and wind_speed <= 40:
        return "Gale"
    elif wind_speed > 40 and wind_speed <= 50:
        return "Strong gale"
    else:
        return "Storm"

import geocoder
from geopy.geocoders import Nominatim

# Initialize geolocator
geolocator = Nominatim(user_agent="geoapi")
class GeoLocation:
    def __init__(self, latlng):
        if latlng:
            self.latitude = latlng[0]
            self.longitude = latlng[1]
        else:
            self.latitude = None
            self.longitude = None

# Get location from IP
def get_location():
    # Try using geocoder
    g = geocoder.ip('me')
    
    if g.latlng:
        location = GeoLocation(g.latlng)
    else:
        location = None
    
    return location


# Check if latlng is available
location = get_location()
if location:

    # Use geopy to reverse geocode the coordinates
    newLoc = geolocator.reverse((location.latitude, location.longitude), language='en', exactly_one=True)
    
    # Extract the address
    if newLoc:
        address = newLoc.raw.get('address', {})
        county = address.get('county') if address.get('county') else address.get('city', '')
        county = county + ", " if county else ''
        state = address.get('state', 'Not available')
        country = address.get('country', 'Not available')
        
        # Format the location string
        place = str(county.title() + str(state).title() + ', ' + str(country).title())
        print(place)
    else:
        place = "Florida, United States"
else:
    place = "Florida, United States"

base_url = "https://api.open-meteo.com/v1/forecast"


params = {
    "latitude": location.latitude,
    "longitude": location.longitude,
    "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m", "apparent_temperature", "weather_code"],
	"hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
	"daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "precipitation_probability_mean"],
	"temperature_unit": "fahrenheit",
	"wind_speed_unit": "mph",
	"precipitation_unit": "inch",
	"timezone": "America/New_York"
    
}

# Declare global variables
temperature = None
wind_speed = None
weather_code = None
data = None
max_temp = None
min_temp = None
sunrise = None
sunset = None
precipitaion = None
precipPercent = None
feelsLike = None

def stripTime(time):
    # Convert to datetime object
    datetime_obj = datetime.fromisoformat(time)
    # Extract and format the time
    return datetime_obj.strftime("%I:%M %p")

def get_weather_data():
    global temperature, wind_speed, weather_code, data, max_temp, min_temp, sunrise, sunset, precipitaion, precipPercent, feelsLike

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        pretty_json = json.dumps(data, indent=4)
        with open("weather_data.json", "w") as file:
            file.write(pretty_json)
        print("Success")

        current = data.get('current', {})
        
        temperature = current.get('temperature_2m', 'N/A')
        feelsLike = current.get('apparent_temperature', 'N/A')
        precipitaion = current.get('precipitation', 'N/A')
        wind_speed = current.get('wind_speed_10m', 'N/A')
        weather_code = current.get('weather_code', 'N/A')
        max_temp = data.get('daily', {}).get('temperature_2m_max', [])[0]
        min_temp = data.get('daily', {}).get('temperature_2m_min', [])[0]
        sunrise = stripTime(data.get('daily', {}).get('sunrise', [])[0])
        sunset = stripTime(data.get('daily', {}).get('sunset', [])[0])
        precipPercent = data.get('daily', {}).get('precipitation_probability_mean', [])[0]

        print("Current Weather Data:")
        print(f"Temperature: {temperature}°F")
        print(f"Wind Speed: {wind_speed} mph")
        print(f"Weather Code: {weather_code}")
    else:
        print("Error fetching weather data.")


def getChange(dataType, wantedType):
    hour = datetime.now().hour
    pre = data.get('hourly', {}).get(dataType, [])[hour-1]
    return round((wantedType - pre),2)
def update():
    print(place)
    try:
        global location
        global params
        
        # Perform geocoding (convert place name to latitude and longitude)
        location = geolocator.geocode(place)
        
        if location is None:
            raise ValueError("Location not found.")
        
        params["latitude"] = location.latitude
        params["longitude"] = location.longitude
        
        # Perform reverse geocoding (convert latitude and longitude to address)
        newLoc = geolocator.reverse((location.latitude, location.longitude), language='en', exactly_one=True)
        
        if newLoc is None:
            raise ValueError("Unable to reverse geocode coordinates.")
        
        address = newLoc.raw.get('address', {})
        
        # Get county, state, and country with fallback values
        county = address.get('county') if address.get('county') else address.get('city', '')
        county = county + ", " if county else ''
        state = address.get('state', 'Not available')
        country = address.get('country', 'Not available')
        
        # Display the location in markdown
        placeholder.markdown(f"### Displaying Weather For: {county.title() + str(state).title() + ', ' + str(country).title()}", unsafe_allow_html=True)
        
        # Fetch and display weather data
        get_weather_data()
        
        # Display weather phrase
        resp.text(weather_phrases.get(weather_code, "Unknown Weather"))
        return weather_code
    except ValueError as ve:
        errorHolder.error(f"Error: {ve}")
    
    except Exception as e:
        errorHolder.error(f"An unexpected error occurred: {e}")

with st.container():
    errorHolder = st.empty()

with st.container():
    col1, col2 = st.columns([3, 1], border=True)  # Adjust column widths
    with col1:
        placeholder = st.empty()
        placeholder.markdown(f"### Displaying Weather For: {place}", unsafe_allow_html=True)
        resp = st.empty()
        resp.text("Go outside! It's sunny!")
    place = col2.text_input("Update Location:", value=place, on_change=update(), placeholder="Enter a location")

    left, middle, right = st.columns([1.2,1,1], border=True)


    update()
    with left:
        lSide, rSide = st.columns(2, vertical_alignment="center")
        with lSide:
            st.image("icons/{}.png".format(weather_code if weather_code not in [None, "N/A"] else 0), width=200)
            #fallback
            description = weather_codes.get(weather_code, "Unknown Weather")
            st.markdown(f"<h4 style='color: #FFFFFF; margin-left: 2.15em; text-decoration: underline 3px white; text-align: center;'>{description}</h4>", unsafe_allow_html=True)
        with rSide:
            rSide.metric(label="Temperature", value="{} °F".format(temperature), delta="{} °F from past hour".format(getChange('temperature_2m', temperature)))
            rSide.metric(label="Feels Like", value="{} °F".format(feelsLike), delta="{} °F difference".format(round((feelsLike - temperature), 2)), delta_color="off")
            rSide.metric(label="Max Temperature", value="{} °F".format(max_temp))
            rSide.metric(label="Min Temperature", value="{} °F".format(min_temp))

    middle.metric(label="Humidity", value="{}%".format(data.get('current', {}).get('relative_humidity_2m', 'N/A')), delta="{}% from past hour".format(getChange('relative_humidity_2m', data.get('current', {}).get('relative_humidity_2m', 'N/A'))))       
    middle.metric(label="Chance Of Precipitation", value="{}%".format(precipPercent))
    middle.metric(label="Precipitation", value="{} in".format(precipitaion))
    middle.metric(label="Wind Speed", value="{} mph: {}".format(wind_speed, (get_wind_condition(wind_speed)).title()), delta="{} mph from past hour".format(getChange('wind_speed_10m', wind_speed)))
    
    with right:
        st.metric(label="Sunrise", value=sunrise)
        st.metric(label="Sunset", value=sunset)
        
        songHolder = st.empty()
        musicHolder = st.empty()
        name = "Skyfall"
        artist = "Adele"
        audio_file = "downloads/{}.mp3".format(name)

        htmlName = """<div class="holder"><div class="text">Now Playing: <span class="highlight-text">{}</span></div><div class="text1"><i>{}</i></div></div>""".format(name, artist)
        songHolder.markdown(htmlName, unsafe_allow_html=True)
        musicHolder.audio(audio_file, format='audio/mp3', loop=True, autoplay=True)

def doSong():
        global weather_code
        song_list = next((songs for codes, songs in weather_music.items() if weather_code in codes), [])
        if song_list:
            print("yes")
            song = song_list[random.randrange(0, len(song_list))]  # Select the first song from the list
            name, artist = song.rsplit(" – ", 1)  # Split the song and artist
            audio_file = f"downloads/{name}.mp3"  # Update the audio file path
            htmlName = """<div class="holder"><div class="text">Now Playing: <span class="highlight-text">{}</span></div><div class="text1"><i>{}</i></div></div>""".format(name, artist)
            songHolder.markdown(htmlName, unsafe_allow_html=True)
            musicHolder.audio(audio_file, format='audio/mp3', loop=True, autoplay=True)
        else:
            print("No")
            songHolder.markdown("<div class='holder'><div class='text'>No music available for this weather.</div></div>", unsafe_allow_html=True)

doSong()

code = weather_code

while True:
    time.sleep(45)
    newCode = update()
    if newCode != code:
        doSong()
        code = newCode
