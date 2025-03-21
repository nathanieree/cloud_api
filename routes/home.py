from flask import Blueprint, render_template, request, redirect, url_for
import requests

home_bp = Blueprint("home", __name__)

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon?limit=150"

@home_bp.route('/')
def home():
    """Fetch list of Pokémon and render them on the homepage."""
    response = requests.get(POKEAPI_URL)
    if response.status_code == 200:
        data = response.json()
        pokemon_list = []

        # Collect basic info (name, image, id)
        for item in data['results']:
            pokemon_id = item['url'].split('/')[-2]  # Extract ID from URL
            pokemon_list.append({
                "name": item['name'].capitalize(),
                "image": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png",
                "id": pokemon_id
            })

        return render_template('index.html', pokemon_list=pokemon_list)
    return "Error fetching Pokémon data."

@home_bp.route('/pokemon', methods=['GET'])
def search_pokemon():
    """Handle search form to look up Pokémon by name or ID."""
    query = request.args.get('name', '').strip().lower()

    if not query:
        return redirect(url_for('home.home'))

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{query}")

    if response.status_code == 200:
        return redirect(url_for('pokemon.pokemon_details', name=query))

    return render_template('not_found.html', name=query), 404
