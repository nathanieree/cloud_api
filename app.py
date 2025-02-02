from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='template', static_folder='static')

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon?limit=50"

@app.route('/')
def home():
    """Fetch list of Pokémon and render them on the homepage."""
    response = requests.get(POKEAPI_URL)
    if response.status_code == 200:
        data = response.json()
        pokemon_list = []
        
        # Collect basic info (name, image, id)
        for item in data['results']:
            pokemon_id = item['url'].split('/')[-2]
            pokemon_list.append({
                "name": item['name'].capitalize(),
                "image": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png",
                "id": pokemon_id
            })
        
        return render_template('index.html', pokemon_list=pokemon_list)
    return "Error fetching Pokémon data."

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
            "types": [t['type']['name'] for t in data['types']]
        }
        return render_template('pokemon.html', pokemon=pokemon_info)
    else:
        return render_template('not_found.html', name=name), 404


if __name__ == '__main__':
    app.run(debug=True)
