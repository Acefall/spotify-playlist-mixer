from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.endOfPattern import EndOfPattern
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.concatenate import Concatenate
from spotify_playlist_mixer.source.takeN import TakeN
from spotify_playlist_mixer.source.loop import Loop
from spotify_playlist_mixer.source.repeatN import RepeatN
import pytest

def test_loop_until_out_of_tracks():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3", "s4", "s5"])
    takeN = TakeN(2, playlist)

    repeatN = Loop(takeN)

    assert next(repeatN) == "s1"
    assert next(repeatN) == "s2"
    assert next(repeatN) == "s3"
    assert next(repeatN) == "s4"
    assert next(repeatN) == "s5"

    with pytest.raises(OutOfTracks) as e_info:
        next(repeatN)


def test_loop_over_two_take_two():
    playlist1 = SpotifyPlaylistMock(["s1", "s2", "s3", "s4", "s5"])
    playlist2 = SpotifyPlaylistMock(["b1", "b2", "b3", "b4", "b5"])
    takeN1 = TakeN(2, playlist1)
    takeN2 = TakeN(2, playlist2)

    concatenate = Concatenate([takeN1, takeN2])
    loop = Loop(concatenate)

    assert next(loop) == "s1"
    assert next(loop) == "s2"
    assert next(loop) == "b1"
    assert next(loop) == "b2"
    assert next(loop) == "s3"
    assert next(loop) == "s4"
    assert next(loop) == "b3"
    assert next(loop) == "b4"
    assert next(loop) == "s5"

    with pytest.raises(OutOfTracks) as e_info:
        next(loop)
