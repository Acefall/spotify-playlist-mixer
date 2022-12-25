from spotifyPlaylistMixer import SpotifyPlaylistMixer
from repeatingPattern import RepeatingPattern
from playlist import Playlist
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import spotipySecrets

scope = "user-library-read playlist-modify-private playlist-modify-public"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(spotipySecrets.client_id,
                              spotipySecrets.client_secret,
                              redirect_uri="http://localhost:8080",
                              scope=scope))

with open('dj.json') as configFile:
    config = json.load(configFile)


mixer = SpotifyPlaylistMixer(sp, config["spotifyId"])

playlists = {}
for source in config["sources"]:
    playlists[source["patternKey"]] = Playlist(sp, source["url"])

pattern = RepeatingPattern(
    config["pattern"])

mixer.mix(config["newPlaylistName"], playlists, pattern)
