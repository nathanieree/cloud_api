from flask import Blueprint, jsonify, request,render_template, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random

# Create a Blueprint for Spotify
spotify_bp = Blueprint('spotify', __name__)


# Spotify API credentials
SPOTIFY_CLIENT_ID = "d824c633863e4eb1abd209f3a5eb3955"
SPOTIFY_CLIENT_SECRET = "d824c633863e4eb1abd209f3a5eb3955"

# Authenticate using Client Credentials Flow
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))


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


# Home route to display playlists
@spotify_bp.route('/spotify')
def index():
    """Display all playlists on an HTML page."""
    return render_template('spotify.html', playlists=POKEMON_PLAYLISTS)

# Add a new playlist
@spotify_bp.route('/spotify/add', methods=['POST'])
def add_playlist():
    """Add a new Pokémon playlist."""
    pokemon_type = request.form.get('pokemon_type')
    playlist_id = request.form.get('playlist_id')

    if pokemon_type and playlist_id:
        POKEMON_PLAYLISTS[pokemon_type] = playlist_id

    return redirect(url_for('spotify.index'))

# Delete a playlist
@spotify_bp.route('/spotify/delete/<pokemon_type>')
def delete_playlist(pokemon_type):
    """Delete a Pokémon playlist."""
    if pokemon_type in POKEMON_PLAYLISTS:
        del POKEMON_PLAYLISTS[pokemon_type]

    return redirect(url_for('spotify.index'))

# Update an existing playlist
@spotify_bp.route('/spotify/update/<pokemon_type>', methods=['POST'])
def update_playlist(pokemon_type):
    """Update a Pokémon playlist."""
    new_playlist_id = request.form.get('playlist_id')

    if pokemon_type in POKEMON_PLAYLISTS and new_playlist_id:
        POKEMON_PLAYLISTS[pokemon_type] = new_playlist_id

    return redirect(url_for('spotify.index'))



# 2️⃣ Route: Get a random Pokémon-themed playlist
@spotify_bp.route('/spotify/random-playlist', methods=['GET'])
def random_pokemon_playlist():
    """Returns a random Pokémon-type playlist."""
    try:
        random_type = random.choice(list(POKEMON_PLAYLISTS.keys()))
        playlist_id = POKEMON_PLAYLISTS[random_type]
        
        return jsonify({"pokemon_type": random_type, "playlist_id": playlist_id})
    except Exception as e:
        print(f"Random Playlist Error: {str(e)}")  # Debugging
        return jsonify({"error": "Failed to fetch random playlist."}), 500


