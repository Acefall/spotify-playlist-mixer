from spotifyPlaylistMixer import SpotifyPlaylistMixer
from repeatingPattern import RepeatingPattern
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

with open('dj.json') as configFile:
    config = json.load(configFile)

if "seed" in config.keys():
    random.seed(config["seed"])


mixer = SpotifyPlaylistMixer(sp, config["spotifyId"])

playlists = {}
for source in config["sources"]:
    playlists[source["patternKey"]] = SpotifyPlaylist(sp, source["url"])

pattern = RepeatingPattern(
    config["pattern"])

mixer.mix(config["newPlaylistName"], playlists, pattern)
