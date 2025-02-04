import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
SPOTIFY_CLIENT_ID = "d824c633863e4eb1abd209f3a5eb3955"
SPOTIFY_CLIENT_SECRET = "d824c633863e4eb1abd209f3a5eb3955"

# Authenticate using Client Credentials Flow
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))
