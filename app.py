from flask import Flask, render_template, request, redirect, url_for
import requests
from weather import get_weather, match_weather_to_pokemon_type  # Import weather functions
from wikipedia import get_pokemon_summary # Import the Wikipedia function
from spotify import get_playlist_for_pokemon


app = Flask(__name__, template_folder='template', static_folder='static')

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon?limit=100"


@app.route('/')
def home():
    """Fetch list of Pokémon and render them on the homepage."""
    response = requests.get(POKEAPI_URL)
    if response.status_code == 200:
        data = response.json()
        pokemon_list = []
        
        # Collect basic info (name, image, id)
        for item in data['results']:
            pokemon_id = item['url'].split('/')[-2] # Extract ID from URL
            pokemon_list.append({
                "name": item['name'].capitalize(),
                "image": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png",
                "id": pokemon_id
            })
        
        return render_template('index.html', pokemon_list=pokemon_list)
    return "Error fetching Pokémon data."

@app.route('/pokemon', methods=['GET'])
def search_pokemon():
    """Handle search form to look up Pokémon by name or ID."""
    query = request.args.get('name', '').strip().lower()

    if not query:
        return redirect(url_for('home'))

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{query}")

    if response.status_code == 200:
        return redirect(url_for('pokemon_details', name=query))

    return render_template('not_found.html', name=query), 404

@app.route('/pokemon/<name>')
def pokemon_details(name):
    """Fetch detailed info of a specific Pokémon and display on the details page."""
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
        spotify_playlist_id = get_playlist_for_pokemon(pokemon_type)
        
        return render_template('pokemon.html', pokemon=pokemon_info, matched_weather=matched_weather, summary=summary, spotify_playlist_id=spotify_playlist_id)
    
    return render_template('not_found.html', name=name), 404

@app.route('/weather', methods=['GET'])
def weather_page():
    """Fetch and display weather data based on user input."""
    city = request.args.get('city', '').strip()
    
    if not city:
        return render_template('weather.html')  # Show the search form if no input
    
    weather_data = get_weather(city)
    if weather_data:
        return render_template('weather.html', city=city, weather=weather_data["condition"], temperature=weather_data["temperature"])
    
    return render_template('weather.html', city=city, weather="Not found", temperature="N/A")


if __name__ == '__main__':
    app.run(debug=True)
