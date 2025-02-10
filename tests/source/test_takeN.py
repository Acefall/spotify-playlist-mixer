from spotify_playlist_mixer.source.takeN import TakeN
from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.endOfPattern import EndOfPattern
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.spotifyPlaylist import SpotifyPlaylist
from spotify_playlist_mixer.derserializer import Deserializer
from spotify_playlist_mixer.serializer import Serializer

import pytest

def test_take_zero_throws_with_first_call():
    playlist = SpotifyPlaylistMock(["s1", "s2"])

    takeN = TakeN(0, playlist)

    with pytest.raises(StopIteration) as e_info:
        next(takeN)

def test_take_n_throws_after_n_plus_one_calls():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3", "s4", "s5"])

    takeN = TakeN(3, playlist)

    assert next(takeN) == "s1"
    assert next(takeN) == "s2"
    assert next(takeN) == "s3"

    # Throws at n+1st call
    with pytest.raises(StopIteration) as e_info:
        next(takeN)

    # Continues to throw
    with pytest.raises(StopIteration) as e_info:
        next(takeN)

def test_resets_after_is_resetted_after_throw():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3", "s4", "s5", "s6", "s7"])

    takeN = TakeN(3, playlist)

    assert next(takeN) == "s1"
    assert next(takeN) == "s2"
    assert next(takeN) == "s3"

    # Throws at n+1st call
    with pytest.raises(StopIteration) as e_info:
        next(takeN)

    takeN.reset_pattern()

    assert next(takeN) == "s4"
    assert next(takeN) == "s5"
    assert next(takeN) == "s6"

    # throws again
    with pytest.raises(StopIteration) as e_info:
        next(takeN)

def test_resets_after_is_resetted_before_throw():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3", "s4", "s5", "s6", "s7"])

    takeN = TakeN(3, playlist)

    assert next(takeN) == "s1"
    assert next(takeN) == "s2"
    takeN.reset_pattern()
    assert next(takeN) == "s3"
    assert next(takeN) == "s4"
    assert next(takeN) == "s5"

    with pytest.raises(StopIteration) as e_info:
        next(takeN)

def test_serialization_and_deserialization_happy_path():
    playlist = SpotifyPlaylistMock([1, 2, 3, 4])
    takeN = TakeN(3, playlist)

    serializer = Serializer()
    serialized = serializer.serialize(takeN)

    deserializer = Deserializer()
    deserializer.class_map["SpotifyPlaylistMock"] = SpotifyPlaylistMock
    deserialized = deserializer.deserialize(serialized)

    assert isinstance(deserialized, TakeN)
    
    for originalTrack, deserializedTrack in zip(takeN, deserialized):
        assert originalTrack == deserializedTrack

    with pytest.raises(EndOfPattern) as e_info:
        next(deserialized)

    takeN.reset_pattern()
    deserialized.reset_pattern()

    for originalTrack, deserializedTrack in zip(takeN, deserialized):
        assert originalTrack == deserializedTrack
    
    with pytest.raises(OutOfTracks) as e_info:
        next(deserialized)

