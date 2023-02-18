from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.filter.booleanFilter import BooleanFilter
from spotify_playlist_mixer.track import Track
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
import pytest


@pytest.fixture
def tracks():
    # Set up a list of tracks
    tracks = [
        Track(None, {
            "id": "123",
            "name": "Volver a Comenzar",
            "duration_ms": 276626,
            "popularity": 44,
            "explicit": False
        }),
        Track(None, {
            "id": "456",
            "name": "Volver a Caminar",
            "duration_ms": 276626,
            "popularity": 44,
            "explicit": True
        }),
        Track(None, {
            "id": "789",
            "name": "Volver a Cocinar",
            "duration_ms": 276626,
            "popularity": 44,
            "explicit": False
        })
    ]
    return tracks

def test_empty_source():
    playlist = SpotifyPlaylistMock([])

    explicitFilter = BooleanFilter(playlist, lambda track: track.explicit, True)

    with pytest.raises(OutOfTracks) as e_info:
        next(explicitFilter)

def test_lambda_always_returns_true(tracks):
    playlist = SpotifyPlaylistMock(tracks)

    explicitFilter = BooleanFilter(playlist, lambda track: True, True)

    assert next(explicitFilter).id == "123"
    assert next(explicitFilter).id == "456"
    assert next(explicitFilter).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(explicitFilter)


def test_filters_out_unwanted_tracks(tracks):
    playlist = SpotifyPlaylistMock(tracks)

    explicitFilter = BooleanFilter(playlist, lambda track: track.explicit, False)

    assert next(explicitFilter).id == "123"
    assert next(explicitFilter).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(explicitFilter)
