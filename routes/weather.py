import requests
from flask import Blueprint, render_template, request

weather_bp = Blueprint("weather", __name__)

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

# Define weather effects on Pokémon battles
WEATHER_EFFECTS = {
    "Clear": {"boost": "Fire", "nerf": "Water"},
    "Rain": {"boost": "Water", "nerf": "Fire"},
    "Thunderstorm": {"boost": "Electric", "nerf": "Ground"},
    "Clouds": {"boost": "Grass", "nerf": "Fire"},
    "Snow": {"boost": "Ice", "nerf": "Rock"},
    "Dust": {"boost": "Ground", "nerf": "Flying"},
    "Sand": {"boost": "Rock", "nerf": "Grass"},
    "Fog": {"boost": "Ghost", "nerf": "Psychic"},
    "Wind": {"boost": "Flying", "nerf": "Rock"},
    "Haze": {"boost": "Psychic", "nerf": "Dark"},
    "Mist": {"boost": "Fairy", "nerf": "Poison"}
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
    return TYPE_WEATHER_MAPPING.get(pokemon_type.lower(), "Unknown")

def get_weather_effect(weather_condition):
    """Ensure weather condition is capitalized before checking effects."""
    weather_condition = weather_condition.capitalize()  # 🔥 Fix case mismatch
    return WEATHER_EFFECTS.get(weather_condition, {"boost": "None", "nerf": "None"})


# ✅ **Route 1: Weather Page (Renders weather.html)**
@weather_bp.route('/weather', methods=['GET'])
def weather_page():
    city = request.args.get('city', '').strip()
    
    if not city:
        return render_template('weather.html')

    weather_data = get_weather(city)
    return render_template(
        'weather.html',
        city=city,
        weather=weather_data["condition"] if weather_data else "Not found",
        temperature=weather_data["temperature"] if weather_data else "N/A"
    )


# ✅ **Route 2: Get Recommended Weather for a Pokémon Type**
@weather_bp.route('/weather/pokemon/<pokemon_type>', methods=['GET'])
def weather_for_pokemon_type(pokemon_type):
    recommended_weather = match_weather_to_pokemon_type(pokemon_type)
    
    return render_template(
        'weather.html',
        pokemon_type=pokemon_type.capitalize(),
        matched_weather=recommended_weather
    )


# ✅ **Route 3: Get Pokémon Battle Effects Based on Weather**
@weather_bp.route('/weather/effect/<pokemon_type>', methods=['GET'])
def weather_effect(pokemon_type):
    # Convert Pokémon type to weather condition
    weather_condition = TYPE_WEATHER_MAPPING.get(pokemon_type.lower(), "Unknown")

    # Debugging (Print to Console)
    print(f"Received Pokémon Type: {pokemon_type}")
    print(f"Mapped Weather Condition: {weather_condition}")

    # Get the effects based on weather condition
    effects = get_weather_effect(weather_condition)

    return render_template(
        'weather.html',
        weather_condition=weather_condition,
        boost=effects["boost"],
        nerf=effects["nerf"]
    )
