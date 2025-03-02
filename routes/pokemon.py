from flask import Blueprint, render_template
import requests
from routes.wikipedia import get_pokemon_summary  # Wikipedia API function
from routes.spotify import get_playlist_for_pokemon  # Spotify API function
from routes.weather import match_weather_to_pokemon_type  # Weather function

pokemon_bp = Blueprint("pokemon", __name__)

@pokemon_bp.route('/pokemon/<name>')
def pokemon_details(name):
    """Fetch detailed info of a specific Pokémon and display it."""
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")

    if response.status_code == 200:
        data = response.json()
        pokemon_info = {
            "name": data['name'].capitalize(),
            "image": data['sprites']['front_default'],
            "height": data['height'],
            "weight": data['weight'],
            "abilities": [ability['ability']['name'] for ability in data['abilities']],
            "types": [t['type']['name'] for t in data['types']],
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
        }

        # Fetch Pokémon summary from Wikipedia
        summary = get_pokemon_summary(pokemon_info['name'])

        # Match Pokémon type with weather
        pokemon_type = pokemon_info['types'][0]
        matched_weather = match_weather_to_pokemon_type(pokemon_type)

        # Get Spotify Playlist
        spotify_playlist_id = get_playlist_for_pokemon(pokemon_type)

        return render_template(
            'pokemon.html',
            pokemon=pokemon_info,
            matched_weather=matched_weather,
            summary=summary,
            spotify_playlist_id=spotify_playlist_id
        )

    return render_template('not_found.html', name=name), 404
