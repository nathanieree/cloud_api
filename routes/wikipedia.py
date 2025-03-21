import wikipediaapi
from flask import Blueprint, render_template

wikipedia_bp = Blueprint("wikipedia", __name__)


# Initialize the Wikipedia API with a custom user-agent
wiki = wikipediaapi.Wikipedia(
    language='en', 
    user_agent='PokémonApp/1.0'
)

def get_pokemon_summary(pokemon_name):
    """Fetch the Wikipedia summary for the given Pokémon name."""
    try:
        # Fetch the page for the Pokémon
        page = wiki.page(pokemon_name)

        if not page.exists():
            return f"No Wikipedia page found for {pokemon_name}."

        # Extract the summary (first 2 sentences)
        summary = page.summary.split('.')[0:2]  # First two sentences
        return '. '.join(summary) + '.'

    except Exception as e:
        return f"An error occurred: {e}"
