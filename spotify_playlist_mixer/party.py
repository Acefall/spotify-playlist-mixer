from source.spotifyPlaylist import SpotifyPlaylist
from source.recentlyPlayed import RecentlyPlayed
from source.takeN import TakeN
from source.concatenate import Concatenate
from source.setMinus import SetMinus
from source.repeatN import RepeatN
from source.loop import Loop
from source.filter.numericRangeFilter import NumericRangeFilter
from source.filter.distinctFilter import DistinctFilter
from source.filter.booleanFilter import BooleanFilter
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
salsa = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/6SzueO7QgQjoPicIO9Lkqn?si=583b8f8a58804bb7", random)
bachata = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/5SqR3iQ1rvzjjB8vEPlF8d?si=214125cac5744fd7", random)
kizomba = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/37i9dQZF1DX1l6qs3gcM4U?si=075ff6e61bc24fd0", random)
kizombaSensual = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/4VFLaOUZDWFsDWbZmCpqP3?si=b48dc3c40720435b", random)

salsa = SetMinus(salsa, recentlyPlayed)
bachata = SetMinus(bachata, recentlyPlayed)
kizomba = SetMinus(kizomba, recentlyPlayed)
kizombaSensual = SetMinus(kizombaSensual, recentlyPlayed)

distinctFilter = DistinctFilter()
salsa = BooleanFilter(salsa, lambda track: distinctFilter.filter(track))
bachata = BooleanFilter(bachata, lambda track: distinctFilter.filter(track))
kizomba = BooleanFilter(kizomba, lambda track: distinctFilter.filter(track))
kizombaSensual = BooleanFilter(kizombaSensual, lambda track: distinctFilter.filter(track))

salsaPattern = TakeN(3, salsa)
bachataPattern = TakeN(3, bachata)
kizombaSensualPattern = TakeN(2, kizomba)
kizombaPattern = TakeN(1, kizomba)

sbk = Concatenate([salsaPattern, bachataPattern, kizombaSensualPattern, kizombaPattern])

playlist = Loop(sbk)

mixer  = SpotifyPlaylistMixer(sp, spotifyId)
mixer.create("Party 2024-09-07", playlist)

print("Done generating")