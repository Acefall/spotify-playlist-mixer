from source.spotifyPlaylist import SpotifyPlaylist
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import spotipySecrets
import random

scope = "user-library-read playlist-modify-private playlist-modify-public"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(spotipySecrets.client_id,
                              spotipySecrets.client_secret,
                              redirect_uri="http://localhost:8080",
                              scope=scope))

playlist = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/3RHSYjPpPPPWnl5JsVkNah?si=2410f670fc2643b0")
tracks = []
for track in playlist:
    print(track)
    tracks.append(track)

print(len(tracks))