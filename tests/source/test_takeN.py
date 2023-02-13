from spotify_playlist_mixer.source.takeN import TakeN
from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
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

