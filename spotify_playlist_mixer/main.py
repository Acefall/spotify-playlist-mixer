from source.spotifyPlaylist import SpotifyPlaylist
from source.takeN import TakeN
from source.concatenate import Concatenate
from source.repeatN import RepeatN
from source.loop import Loop
from source.filter.numericRangeFilter import NumericRangeFilter
from source.filter.booleanFilter import BooleanFilter
from spotifyPlaylistMixer import SpotifyPlaylistMixer
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import spotipySecrets
import random

spotifyId = "acefall"
newPlaylistName = "Mixed Playlist"


scope = "user-library-read playlist-modify-private playlist-modify-public"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(spotipySecrets.client_id,
                              spotipySecrets.client_secret,
                              redirect_uri="http://localhost:8080",
                              scope=scope))

salsa = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/5Db6luvdhq3bEGwX3zcI5P?si=1e777cc298fe4fc4")
bachata = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/4rPVgVb4xNOpexM22v5I72?si=8a4902de321a4f93")
kizomba = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/0RPAReDJdaECIrco82WuhC?si=388dc32d20cc43b0")
zouk = SpotifyPlaylist(sp, "https://open.spotify.com/playlist/3BnuWDbMlEHzEnyC3zwS4q?si=9a52f63277124ee0")

nonExplicitBachata = BooleanFilter(bachata, lambda track: track.explicit, False)
highEnergyKizomba = NumericRangeFilter(kizomba, lambda track: track.get_audio_features().energy, 0.75, 1)

salsaPattern = TakeN(3, salsa)
bachataPattern = TakeN(3, nonExplicitBachata)
kizombaPattern = TakeN(3, highEnergyKizomba)
zoukPattern = TakeN(2, zouk)

sbk = Concatenate([salsaPattern, bachataPattern, kizombaPattern])
sbk3 = RepeatN(3, sbk)
sbkAndZouk = Concatenate([sbk3, zoukPattern])


playlist = Loop(sbkAndZouk)

mixer  = SpotifyPlaylistMixer(sp, spotifyId)
mixer.create("New Mixed Playlist", playlist)

print("Done generating")