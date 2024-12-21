from spotify_playlist_mixer.source.takeN import TakeN
from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.spotifyPlaylist import SpotifyPlaylist
from spotify_playlist_mixer.derserializer import Deserializer
from spotify_playlist_mixer.source.shuffle import Shuffle
import random

import pytest

def test_shuffle_shuffles_the_tracks():
    random.seed(123)

    originalTracks = ["s1", "s2", "s3"]
    playlist = SpotifyPlaylistMock(originalTracks)

    shuffled = Shuffle(playlist, random)

    queriedTracks = []

    shuffledIt = iter(shuffled)
    queriedTracks.append(next(shuffledIt))
    queriedTracks.append(next(shuffledIt))
    queriedTracks.append(next(shuffledIt))

    with pytest.raises(OutOfTracks) as e_info:
        next(shuffledIt)

    difference = set(queriedTracks) ^ set(originalTracks)
    assert not difference