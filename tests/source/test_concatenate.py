from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.endOfPattern import EndOfPattern
from spotify_playlist_mixer.source.concatenate import Concatenate
from spotify_playlist_mixer.source.takeN import TakeN
from spotify_playlist_mixer.source.spotifyPlaylist import SpotifyPlaylist
from spotify_playlist_mixer.derserializer import Deserializer
from spotify_playlist_mixer.serializer import Serializer
import pytest

def test_test_single_source_is_used_until_the_end():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3"])

    concatenate = Concatenate([playlist])

    assert next(concatenate) == "s1"
    assert next(concatenate) == "s2"
    assert next(concatenate) == "s3"

    with pytest.raises(OutOfTracks) as e_info:
        next(concatenate)

    with pytest.raises(OutOfTracks) as e_info:
        next(concatenate)

def test_two_sources_are_chosen_concatenate():
    playlist1 = SpotifyPlaylistMock(["s1", "s2", "s3", "s4", "s5"])
    playlist2 = SpotifyPlaylistMock(["b1", "b2", "b3", "b4", "b5"])
    takeN1 = TakeN(2, playlist1)
    takeN2 = TakeN(2, playlist2)

    concatenate = Concatenate([takeN1, takeN2])

    assert next(concatenate) == "s1"
    assert next(concatenate) == "s2"
    assert next(concatenate) == "b1"
    assert next(concatenate) == "b2"

    with pytest.raises(EndOfPattern) as e_info:
        next(concatenate)

    with pytest.raises(EndOfPattern) as e_info:
        next(concatenate)

def test_serialization_and_deserialization_happy_path():
    playlist1 = SpotifyPlaylistMock([1, 2, 3])
    playlist2 = SpotifyPlaylistMock([4, 5, 6])
    concatenate = Concatenate([playlist1, playlist2])

    serializer = Serializer()
    serialized = serializer.serialize(concatenate)

    deserializer = Deserializer()
    deserializer.class_map["SpotifyPlaylistMock"] = SpotifyPlaylistMock
    deserialized = deserializer.deserialize(serialized)

    assert isinstance(deserialized, Concatenate)
    
    for originalTrack, deserializedTrack in zip(concatenate, deserialized):
        assert originalTrack == deserializedTrack

    with pytest.raises(OutOfTracks) as e_info:
        next(deserialized)