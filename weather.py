import requests

# OpenWeatherMap API Configuration
OPENWEATHER_API_KEY = "d73c503d37237f00a3dbf896c23b69a4"
OPENWEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

# Define type-weather mapping
TYPE_WEATHER_MAPPING = {
    "fire": "Clear",
    "water": "Rain",
    "electric": "Thunderstorm",
    "grass": "Clouds",
    "ice": "Snow",
    "ground": "Dust",
    "rock": "Sand",
    "ghost": "Fog",
    "flying": "Wind",
    "normal": "Clear",
    "psychic": "Haze",
    "dark": "Fog",
    "fairy": "Mist"
}

def get_weather(city):
    """Fetch weather data for a given city using OpenWeatherMap API."""
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(OPENWEATHER_URL, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        weather_condition = weather_data['weather'][0]['main']
        temperature = weather_data['main']['temp']
        return {"condition": weather_condition, "temperature": temperature}
    
    return None

def match_weather_to_pokemon_type(pokemon_type):
    """Return the recommended weather condition for a given Pokémon type."""
    return TYPE_WEATHER_MAPPING.get(pokemon_type, "Unknown")


