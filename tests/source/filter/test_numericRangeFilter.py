from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.filter.numericRangeFilter import NumericRangeFilter
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

    acousticFilter = NumericRangeFilter(playlist, lambda track: track.get_audio_features().acousticness, 0, 0.5)

    with pytest.raises(OutOfTracks) as e_info:
        next(acousticFilter)

def test_filters_unwanted_tracks(tracks):
    playlist = SpotifyPlaylistMock(tracks)

    acousticFilter = NumericRangeFilter(playlist, lambda track: track.get_audio_features().acousticness, 0, 0.5)

    assert next(acousticFilter).id == "123"
    assert next(acousticFilter).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(acousticFilter)


def test_filters_nothing_when_set_to_maximum_range(tracks):
    playlist = SpotifyPlaylistMock(tracks)

    acousticFilter = NumericRangeFilter(playlist, lambda track: track.get_audio_features().acousticness, 0, 1)

    assert next(acousticFilter).id == "123"
    assert next(acousticFilter).id == "456"
    assert next(acousticFilter).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(acousticFilter)

def test_flipped_lower_and_upper_limit(tracks):
    playlist = SpotifyPlaylistMock(tracks)

    acousticFilter = NumericRangeFilter(playlist, lambda track: track.get_audio_features().acousticness, 0.5, 0)

    assert next(acousticFilter).id == "123"
    assert next(acousticFilter).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(acousticFilter)


def test_chained_filters_act_like_logical_and(tracks):
    playlist = SpotifyPlaylistMock(tracks)

    acousticFilter = NumericRangeFilter(playlist, lambda track: track.get_audio_features().acousticness, 0, 0.5)
    danceabilityFilter = NumericRangeFilter(acousticFilter, lambda track: track.get_audio_features().danceability, 0.75, 1)

    assert next(danceabilityFilter).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(danceabilityFilter)
