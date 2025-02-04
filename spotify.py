from spotify_config import sp

# Predefined Pokémon type-based playlists (you can customize these with actual Spotify playlist IDs)
POKEMON_PLAYLISTS = {
    "fire": "37i9dQZF1DX0b1hHYQtJjp",  # Example: "Hot Hits"
    "water": "37i9dQZF1DX7gIoKXt0gmx",  # Example: "Chill Vibes"
    "electric": "37i9dQZF1DX4eRPd9frC1m",  # Example: "Energy Boost"
    "grass": "37i9dQZF1DWZwtERXCS82H",  # Example: "Nature Sounds"
    "ice": "37i9dQZF1DWVFJtzvDHN4L",  # Example: "Chill Beats"
    "rock": "37i9dQZF1DXcF6B6QPhFDv",  # Example: "Rock Classics"
}

def get_playlist_for_pokemon(pokemon_type):
    """Get a Spotify playlist ID based on Pokémon type."""
    return POKEMON_PLAYLISTS.get(pokemon_type, "37i9dQZF1DXcF6B6QPhFDv")  # Default to Rock Classics
