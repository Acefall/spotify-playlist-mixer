from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.filter.booleanFilter import BooleanFilter
from spotify_playlist_mixer.track import Track
from spotify_playlist_mixer.audioFeatures import AudioFeatures
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
    
    tracks[0].audio_features = AudioFeatures({
        "acousticness": 0,
        "danceability": 0.5,
        "energy": 1
    })

    tracks[1].audio_features = AudioFeatures({
        "acousticness": 1,
        "danceability": 0,
        "energy": 0.5
    })

    tracks[2].audio_features = AudioFeatures({
        "acousticness": 0.5,
        "danceability": 1,
        "energy": 0
    })
    
    return tracks

def test_empty_source():
    playlist = SpotifyPlaylistMock([])

    explicitFilter = BooleanFilter(playlist, "explicit", True)

    with pytest.raises(OutOfTracks) as e_info:
        next(explicitFilter)

def test_filters_out_unwanted_tracks(tracks):
    playlist = SpotifyPlaylistMock(tracks)

    explicitFilter = BooleanFilter(playlist, "explicit", False)

    assert next(explicitFilter).id == "123"
    assert next(explicitFilter).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(explicitFilter)
