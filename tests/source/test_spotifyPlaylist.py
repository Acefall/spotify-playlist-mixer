from spotify_playlist_mixer.source.spotifyPlaylist import SpotifyPlaylist
from spotify_playlist_mixer.deserializationError import DeserializationError

import pytest

def test_to_and_from_dict_happy_path():
    playlist = SpotifyPlaylist(None, "my/nice/playlist")

    playlistDict = playlist.toDict()

    playlistFromDict = SpotifyPlaylist.fromDict(playlistDict)

    assert playlist.url == playlistFromDict.url
