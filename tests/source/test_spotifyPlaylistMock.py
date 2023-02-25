from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
import pytest
import random

def test_throws_out_of_tracks_exception():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3"])

    playlistIt = iter(playlist)
    assert next(playlistIt) == "s1"
    assert next(playlistIt) == "s2"
    assert next(playlistIt) == "s3"

    with pytest.raises(OutOfTracks) as e_info:
        next(playlistIt)

def test_randomness_shuffles_the_tracks():
    random.seed(123)

    originalTracks = ["s1", "s2", "s3"]
    playlist = SpotifyPlaylistMock(originalTracks, random)

    queriedTracks = []

    playlistIt = iter(playlist)
    queriedTracks.append(next(playlistIt))
    queriedTracks.append(next(playlistIt))
    queriedTracks.append(next(playlistIt))

    with pytest.raises(OutOfTracks) as e_info:
        next(playlistIt)

    difference = set(queriedTracks) ^ set(originalTracks)
    assert not difference

    

