from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.filter.numericRangeFilter import NumericRangeFilter
from spotify_playlist_mixer.track import Track
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.serializer import Serializer
from spotify_playlist_mixer.derserializer import Deserializer
import pytest


@pytest.fixture
def tracks():
    # Set up a list of tracks
    tracks = [
        Track(None, {
            "id": "123",
            "name": "Volver a Comenzar",
            "duration_ms": 276626,
            "popularity": 0,
            "explicit": False
        }),
        Track(None, {
            "id": "456",
            "name": "Volver a Caminar",
            "duration_ms": 276626,
            "popularity": 50,
            "explicit": True
        }),
        Track(None, {
            "id": "789",
            "name": "Volver a Cocinar",
            "duration_ms": 276626,
            "popularity": 100,
            "explicit": False
        })
    ]

    return tracks

def test_empty_source():
    playlist = SpotifyPlaylistMock([])

    popularityFilter = NumericRangeFilter(playlist, "popularity", 0, 100)

    with pytest.raises(OutOfTracks) as e_info:
        next(popularityFilter)

def test_filters_unwanted_tracks(tracks):
    playlist = SpotifyPlaylistMock(tracks)

    popularityFilter = NumericRangeFilter(playlist, "popularity", 50, 100)

    assert next(popularityFilter).id == "456"
    assert next(popularityFilter).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(popularityFilter)


def test_filters_nothing_when_set_to_maximum_range(tracks):
    playlist = SpotifyPlaylistMock(tracks)

    popularityFilter = NumericRangeFilter(playlist, "popularity", 0, 100)

    assert next(popularityFilter).id == "123"
    assert next(popularityFilter).id == "456"
    assert next(popularityFilter).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(popularityFilter)

def test_flipped_lower_and_upper_limit(tracks):
    playlist = SpotifyPlaylistMock(tracks)

    popularityFilter = NumericRangeFilter(playlist, "popularity", 50, 100)

    assert next(popularityFilter).id == "456"
    assert next(popularityFilter).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(popularityFilter)


def test_chained_filters_act_like_logical_and(tracks):
    playlist = SpotifyPlaylistMock(tracks)

    popularityFilter = NumericRangeFilter(playlist, "popularity", 50, 100)
    popularityFilter2 = NumericRangeFilter(popularityFilter, "popularity", 75, 100)

    assert next(popularityFilter2).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(popularityFilter2)


def test_serialization_and_deserialization_happy_path(tracks):
    playlist = SpotifyPlaylistMock(tracks)
    popularityFilter = NumericRangeFilter(playlist, "popularity", 50, 100)

    serializer = Serializer()
    serialized = serializer.serialize(popularityFilter)

    deserializer = Deserializer(serializer.getObjects())
    deserializer.class_map["SpotifyPlaylistMock"] = SpotifyPlaylistMock
    deserialized = deserializer.deserialize(serialized)

    assert isinstance(deserialized, NumericRangeFilter)

    for originalTrack, deserializedTrack in zip(popularityFilter, deserialized):
        assert originalTrack.id == deserializedTrack.id

    with pytest.raises(OutOfTracks) as e_info:
        next(deserialized)
