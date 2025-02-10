from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.filter.distinctFilterSet import DistinctFilterSet
from spotify_playlist_mixer.source.filter.distinctFilter import DistinctFilter
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.track import Track
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

def test_distinct_filter_removes_duplictae_tracks_from_a_source(tracks):
    playlist = SpotifyPlaylistMock(tracks + tracks)

    distinctPlaylist = DistinctFilter(playlist)

    assert next(distinctPlaylist).id == "123"
    assert next(distinctPlaylist).id == "456"
    assert next(distinctPlaylist).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(distinctPlaylist)


def test_distinct_filter_removes_duplictae_tracks_from_two_sources(tracks):
    playlist1 = SpotifyPlaylistMock(tracks)
    playlist2 = SpotifyPlaylistMock(tracks)

    distinctFilterSet = DistinctFilterSet()
    distinctSource1 = DistinctFilter(playlist1, distinctFilterSet)
    distinctSource2 = DistinctFilter(playlist2, distinctFilterSet)

    assert next(distinctSource1).id == "123"
    assert next(distinctSource2).id == "456"
    assert next(distinctSource2).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(distinctSource1)

    with pytest.raises(OutOfTracks) as e_info:
        next(distinctSource2)

def test_serialization_and_deserialization_happy_path(tracks):
    playlist1 = SpotifyPlaylistMock(tracks)
    playlist2 = SpotifyPlaylistMock(tracks)

    distinctFilterSet = DistinctFilterSet()
    distinctSource1 = DistinctFilter(playlist1, distinctFilterSet)
    distinctSource2 = DistinctFilter(playlist2, distinctFilterSet)

    serializer = Serializer()
    serialized1 = serializer.serialize(distinctSource1)
    serialized2 = serializer.serialize(distinctSource2)

    deserializer = Deserializer(serializer.getObjects())
    deserializer.class_map["SpotifyPlaylistMock"] = SpotifyPlaylistMock
    deserialized1 = deserializer.deserialize(serialized1)
    deserialized2 = deserializer.deserialize(serialized2)

    assert isinstance(deserialized1, DistinctFilter)
    assert isinstance(deserialized2, DistinctFilter)
    assert next(deserialized1).id == "123"
    assert next(deserialized2).id == "456"
    assert next(deserialized1).id == "789"

    with pytest.raises(OutOfTracks) as e_info:
        next(deserialized1)

    with pytest.raises(OutOfTracks) as e_info:
        next(deserialized2)
