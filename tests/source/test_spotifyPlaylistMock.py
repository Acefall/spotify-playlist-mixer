from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
import pytest
from spotify_playlist_mixer.serializer import Serializer
from spotify_playlist_mixer.derserializer import Deserializer

def test_throws_out_of_tracks_exception():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3"])

    playlistIt = iter(playlist)
    assert next(playlistIt) == "s1"
    assert next(playlistIt) == "s2"
    assert next(playlistIt) == "s3"

    with pytest.raises(OutOfTracks) as e_info:
        next(playlistIt)



def test_serialization_and_deserialization_happy_path():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3"])

    serializer = Serializer()
    serialized = serializer.serialize(playlist)

    deserializer = Deserializer(serializer.getObjects())
    deserializer.class_map["SpotifyPlaylistMock"] = SpotifyPlaylistMock
    deserialized = deserializer.deserialize(serialized)

    assert isinstance(deserialized, SpotifyPlaylistMock)
    for originalTrack, deserializedTrack in zip(playlist, deserialized):
        assert originalTrack == deserializedTrack

    with pytest.raises(OutOfTracks) as e_info:
        next(deserialized)
    

