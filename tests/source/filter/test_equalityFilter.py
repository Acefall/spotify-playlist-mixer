from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.filter.equalityFilter import EqualityFilter
from spotify_playlist_mixer.track import Track
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.serializer import Serializer
from spotify_playlist_mixer.deserializer import Deserializer
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

    explicitFilter = EqualityFilter(playlist, "explicit", True)

    with pytest.raises(OutOfTracks) as e_info:
        next(explicitFilter)


def test_filters_out_unwanted_tracks(tracks):
    playlist = SpotifyPlaylistMock(tracks)

    explicitFilter = EqualityFilter(playlist, "explicit", False)

    assert next(explicitFilter).id == "123"
    assert next(explicitFilter).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(explicitFilter)

def test_serialization_and_deserialization_happy_path(tracks):
    playlist = SpotifyPlaylistMock(tracks)
    explicitFilter = EqualityFilter(playlist, "explicit", False)

    serializer = Serializer()
    serialized = serializer.serialize(explicitFilter)

    deserializer = Deserializer()
    deserializer.class_map["SpotifyPlaylistMock"] = SpotifyPlaylistMock
    deserialized = deserializer.deserialize(serialized)

    assert isinstance(deserialized, EqualityFilter)
    
    for originalTrack, deserializedTrack in zip(explicitFilter, deserialized):
        assert originalTrack.id == deserializedTrack.id

    with pytest.raises(OutOfTracks) as e_info:
        next(deserialized)
