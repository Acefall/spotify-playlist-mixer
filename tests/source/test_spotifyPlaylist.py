from spotify_playlist_mixer.source.spotifyPlaylist import SpotifyPlaylist
from spotify_playlist_mixer.deserializationError import DeserializationError
from spotify_playlist_mixer.derserializer import Deserializer
from spotify_playlist_mixer.serializer import Serializer

import pytest

def test_serialization_and_deserialization_happy_path():
    playlist = SpotifyPlaylist(None, "my/nice/playlist")

    serializer = Serializer()
    serialized = serializer.serialize(playlist)

    deserializer = Deserializer(serializer.getObjects(), None)
    deserialized = deserializer.deserialize(serialized)

    assert isinstance(deserialized, SpotifyPlaylist)
