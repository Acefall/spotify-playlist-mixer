from spotify_playlist_mixer.deserializer import Deserializer
from spotify_playlist_mixer.spotifyPlaylistMixer import SpotifyPlaylistMixer
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import spotipySecrets
import random

spotifyId = "acefall"
newPlaylistName = "Deserialized Playlist"
intputFileNmae = "serializedPlaylist.json"


scope = "user-library-read playlist-modify-private playlist-modify-public user-read-recently-played"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(spotipySecrets.client_id,
                              spotipySecrets.client_secret,
                              redirect_uri="http://localhost:8080",
                              scope=scope))

with open(intputFileNmae, "r") as inputFile:
    deserializer = Deserializer(sp, random)
    playlist = json.load(inputFile)
    mixer  = SpotifyPlaylistMixer(sp, spotifyId)
    mixer.create(newPlaylistName, deserializer.deserialize(playlist))

    print("Done generating")