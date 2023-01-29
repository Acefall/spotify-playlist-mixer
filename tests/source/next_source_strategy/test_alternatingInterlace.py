from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.next_source_strategy.alternatingInterlace import AlternatingInterlace
import pytest

def test_test_single_source_is_chosen_every_time():
    playlist = SpotifyPlaylistMock(["s1", "s2", "s3"])

    alternating = AlternatingInterlace([playlist])

    assert alternating.getNextSource() == playlist
    assert alternating.getNextSource() == playlist
    assert alternating.getNextSource() == playlist
    assert alternating.getNextSource() == playlist

def test_two_sources_are_chosen_alternating():
    playlist1 = SpotifyPlaylistMock(["s1", "s2", "s3"])
    playlist2 = SpotifyPlaylistMock(["b1", "b2", "b3"])

    alternating = AlternatingInterlace([playlist1, playlist2])

    assert alternating.getNextSource() == playlist1
    assert alternating.getNextSource() == playlist2
    assert alternating.getNextSource() == playlist1
    assert alternating.getNextSource() == playlist2
    assert alternating.getNextSource() == playlist1
    assert alternating.getNextSource() == playlist2

def test_many_sources_are_chosen_alternating():
    playlist1 = SpotifyPlaylistMock(["s1", "s2", "s3"])
    playlist2 = SpotifyPlaylistMock(["b1", "b2", "b3"])
    playlist3 = SpotifyPlaylistMock(["k1", "k2", "k3"])
    playlist4 = SpotifyPlaylistMock(["w1", "w2", "w3"])

    alternating = AlternatingInterlace([playlist1, playlist2, playlist3, playlist4])

    assert alternating.getNextSource() == playlist1
    assert alternating.getNextSource() == playlist2
    assert alternating.getNextSource() == playlist3
    assert alternating.getNextSource() == playlist4
    assert alternating.getNextSource() == playlist1
    assert alternating.getNextSource() == playlist2
    assert alternating.getNextSource() == playlist3
    assert alternating.getNextSource() == playlist4