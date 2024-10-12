from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.filter.booleanFilter import BooleanFilter
from spotify_playlist_mixer.source.filter.distinctFilter import DistinctFilter
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.track import Track
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

def test_filter_tracks_which_have_already_been_seen(tracks):
    distinctFilter = DistinctFilter()
    assert distinctFilter.filter(tracks[0]) == True
    assert distinctFilter.filter(tracks[1])
    assert not distinctFilter.filter(tracks[0])
    assert not distinctFilter.filter(tracks[1])
    assert distinctFilter.filter(tracks[2])
    assert not distinctFilter.filter(tracks[2])

def test_distinct_filter_removes_duplictae_tracks_from_a_source(tracks):
    playlist = SpotifyPlaylistMock(tracks + tracks)

    distinctFilter = DistinctFilter()
    distinctSource = BooleanFilter(playlist, lambda track: distinctFilter.filter(track))

    assert next(distinctSource).id == "123"
    assert next(distinctSource).id == "456"
    assert next(distinctSource).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(distinctSource)


def test_distinct_filter_removes_duplictae_tracks_from_two_sources(tracks):
    playlist1 = SpotifyPlaylistMock(tracks)
    playlist2 = SpotifyPlaylistMock(tracks)

    distinctFilter = DistinctFilter()
    distinctSource1 = BooleanFilter(playlist1, lambda track: distinctFilter.filter(track))
    distinctSource2 = BooleanFilter(playlist2, lambda track: distinctFilter.filter(track))

    assert next(distinctSource1).id == "123"
    assert next(distinctSource2).id == "456"
    assert next(distinctSource2).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(distinctSource1)

    with pytest.raises(OutOfTracks) as e_info:
        next(distinctSource2)
