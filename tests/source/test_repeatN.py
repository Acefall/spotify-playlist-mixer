from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.endOfPattern import EndOfPattern
from spotify_playlist_mixer.source.concatenate import Concatenate
from spotify_playlist_mixer.source.takeN import TakeN
from spotify_playlist_mixer.source.repeatN import RepeatN
from spotify_playlist_mixer.source.spotifyPlaylist import SpotifyPlaylist
from spotify_playlist_mixer.derserializer import Deserializer
from spotify_playlist_mixer.serializer import Serializer
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
import pytest

def test_repeat_n_equals_one_has_no_effect():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3", "s4", "s5"])
    takeN = TakeN(2, playlist)

    repeatN = RepeatN(1, takeN)

    assert next(repeatN) == "s1"
    assert next(repeatN) == "s2"

    with pytest.raises(EndOfPattern) as e_info:
        next(repeatN)

    with pytest.raises(EndOfPattern) as e_info:
        next(repeatN)

def test_repeat_two_repeats_once():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3", "s4", "s5"])
    takeN = TakeN(2, playlist)

    repeatN = RepeatN(2, takeN)

    assert next(repeatN) == "s1"
    assert next(repeatN) == "s2"
    assert next(repeatN) == "s3"
    assert next(repeatN) == "s4"

    with pytest.raises(EndOfPattern) as e_info:
        next(repeatN)

    with pytest.raises(EndOfPattern) as e_info:
        next(repeatN)


def test_repeat_zero_throws_at_first_call_to_next():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3", "s4", "s5"])
    takeN = TakeN(2, playlist)

    repeatN = RepeatN(0, takeN)

    with pytest.raises(EndOfPattern) as e_info:
        next(repeatN)

    with pytest.raises(EndOfPattern) as e_info:
        next(repeatN)

def test_reset_pattern():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9"])
    takeN = TakeN(2, playlist)

    repeatN = RepeatN(2, takeN)

    assert next(repeatN) == "s1"
    assert next(repeatN) == "s2"
    assert next(repeatN) == "s3"
    assert next(repeatN) == "s4"

    with pytest.raises(EndOfPattern) as e_info:
        next(repeatN)

    repeatN.reset_pattern()

    assert next(repeatN) == "s5"
    assert next(repeatN) == "s6"
    assert next(repeatN) == "s7"
    assert next(repeatN) == "s8"

    with pytest.raises(EndOfPattern) as e_info:
        next(repeatN)

def test_serialization_and_deserialization_happy_path():
    playlist = SpotifyPlaylistMock([1, 2, 3, 4, 5, 6, 7, 8, 9])
    takeN = TakeN(2, playlist)
    repeat = RepeatN(3, takeN)

    serializer = Serializer()
    serialized = serializer.serialize(repeat)

    deserializer = Deserializer()
    deserializer.class_map["SpotifyPlaylistMock"] = SpotifyPlaylistMock
    deserialized = deserializer.deserialize(serialized)

    assert isinstance(deserialized, RepeatN)
    
    for originalTrack, deserializedTrack in zip(repeat, deserialized):
        assert originalTrack == deserializedTrack

    with pytest.raises(EndOfPattern) as e_info:
        next(deserialized)