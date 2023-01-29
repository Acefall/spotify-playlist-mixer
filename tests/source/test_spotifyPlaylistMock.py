from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
import pytest

def test_throws_out_of_tracks_exception():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3"])

    playlistIt = iter(playlist)
    assert next(playlistIt) == "s1"
    assert next(playlistIt) == "s2"
    assert next(playlistIt) == "s3"

    with pytest.raises(OutOfTracks) as e_info:
        next(playlistIt)

def test_reset_pattern_loops_tracks():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3"])

    playlistIt = iter(playlist)
    assert next(playlistIt) == "s1"
    assert next(playlistIt) == "s2"
    assert next(playlistIt) == "s3"

    with pytest.raises(OutOfTracks) as e_info:
        next(playlistIt)

    playlist.reset_pattern(False)

    assert next(playlistIt) == "s1"
    assert next(playlistIt) == "s2"
    assert next(playlistIt) == "s3"

    with pytest.raises(OutOfTracks) as e_info:
        next(playlistIt)
