from source.spotifyPlaylist import SpotifyPlaylist
from source.recentlyPlayed import RecentlyPlayed
from source.takeN import TakeN
from source.concatenate import Concatenate
from source.setMinus import SetMinus
from source.repeatN import RepeatN
from source.loop import Loop
from source.filter.equalityFilter import EqualityFilter
from source.filter.distinctFilter import DistinctFilter
from source.filter.distinctFilterSet import DistinctFilterSet
from source.shuffle import Shuffle
from spotifyPlaylistMixer import SpotifyPlaylistMixer
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import spotipySecrets
import random

spotifyId = "acefall"
newPlaylistName = "Mixed Playlist"


scope = "user-library-read playlist-modify-private playlist-modify-public user-read-recently-played"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(spotipySecrets.client_id,
                              spotipySecrets.client_secret,
                              redirect_uri="http://localhost:8080",
                              scope=scope))

recentlyPlayed = RecentlyPlayed(sp)
salsa = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/6SzueO7QgQjoPicIO9Lkqn?si=583b8f8a58804bb7")
bachata = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/5SqR3iQ1rvzjjB8vEPlF8d?si=214125cac5744fd7")
kizomba = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/0RPAReDJdaECIrco82WuhC?si=3198b7d436e04547")
kizombaSensual = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/034xxmY8mxDxEZlvTyyD0y?si=8d44f77f116344da")

salsa = Shuffle(salsa, random)
bachata = Shuffle(bachata, random)
kizomba = Shuffle(kizomba, random)
kizombaSensual = Shuffle(kizombaSensual, random)


salsa = SetMinus(salsa, recentlyPlayed)
bachata = SetMinus(bachata, recentlyPlayed)
kizomba = SetMinus(kizomba, recentlyPlayed)
kizombaSensual = SetMinus(kizombaSensual, recentlyPlayed)

distinctFilterSet = DistinctFilterSet()
salsa = DistinctFilter(salsa, distinctFilterSet)
bachata = DistinctFilter(bachata, distinctFilterSet)
kizomba = DistinctFilter(kizomba, distinctFilterSet)
kizombaSensual = DistinctFilter(kizombaSensual, distinctFilterSet)

salsaPattern = TakeN(3, salsa)
bachataPattern = TakeN(3, bachata)
kizombaSensualPattern = TakeN(2, kizomba)
kizombaPattern = TakeN(1, kizomba)

sbk = Concatenate([salsaPattern, bachataPattern, kizombaSensualPattern, kizombaPattern])

playlist = Loop(sbk)

mixer  = SpotifyPlaylistMixer(sp, spotifyId)
mixer.create("Party 2024-09-07", playlist)

print("Done generating")