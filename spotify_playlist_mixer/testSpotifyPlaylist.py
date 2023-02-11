from source.spotifyPlaylist import SpotifyPlaylist
from source.takeN import TakeN
from source.next_source_strategy.concatenate import Concatenate
from source.combine import Combine
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

salsaPl = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/5Db6luvdhq3bEGwX3zcI5P?si=1e777cc298fe4fc4")
bachataPl = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/4rPVgVb4xNOpexM22v5I72?si=8a4902de321a4f93")
kizombaPl = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/0RPAReDJdaECIrco82WuhC?si=388dc32d20cc43b0")
zoukPl = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/3BnuWDbMlEHzEnyC3zwS4q?si=9a52f63277124ee0")

salsaPattern = TakeN(3, salsaPl)
bachataPattern = TakeN(2, salsaPl)
kizombaPattern = TakeN(3, salsaPl)
zoukPattern = TakeN(1, salsaPl)

sbkSources = [salsaPattern, bachataPattern, kizombaPattern]
concatenateSbk = Concatenate(sbkSources)
combineSbk = Combine(sbkSources, concatenateSbk)

rootSources = [combineSbk, zoukPattern]
rootConcatenate = Concatenate(rootSources)

playlist = Combine(rootSources, rootConcatenate)

tracks = []
for track in playlist:
    print(track)
    tracks.append(track)

print(len(tracks))

newPlaylist = sp.user_playlist_create("acefall", "testCombineTakeN")
for i in range(0, len(tracks), 100):
    sp.user_playlist_add_tracks(
        "acefall", newPlaylist["id"], tracks[i:i+100])

print("Done generating")