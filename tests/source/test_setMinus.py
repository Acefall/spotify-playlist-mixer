from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.endOfPattern import EndOfPattern
from spotify_playlist_mixer.source.setMinus import SetMinus
import pytest

def test_empty_second_source_does_not_subtract_anything():
    playlist1 = SpotifyPlaylistMock(["s1", "s2", "s3"])
    playlist2 = SpotifyPlaylistMock([])

    subtracted = SetMinus(playlist1, playlist2)

    assert next(subtracted) == "s1"
    assert next(subtracted) == "s2"
    assert next(subtracted) == "s3"

    with pytest.raises(OutOfTracks) as e_info:
        next(subtracted)


def test_two_equal_sources_result_in_emtpy_list():
    playlist1 = SpotifyPlaylistMock(["s1", "s2", "s3"])
    playlist2 = SpotifyPlaylistMock(["s1", "s2", "s3"])

    subtracted = SetMinus(playlist1, playlist2)

    with pytest.raises(OutOfTracks) as e_info:
        next(subtracted)

def test_happy_path_some_elements_are_subtracted():
    playlist1 = SpotifyPlaylistMock(["s1", "s2", "s3", "s4", "s5"])
    playlist2 = SpotifyPlaylistMock(["s1", "s2", "s5"])

    subtracted = SetMinus(playlist1, playlist2)

    assert next(subtracted) == "s3"
    assert next(subtracted) == "s4"

    with pytest.raises(OutOfTracks) as e_info:
        next(subtracted)
