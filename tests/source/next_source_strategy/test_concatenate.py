from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.next_source_strategy.concatenate import Concatenate
import pytest

def test_single_source_is_chosen_again_after_out_of_tracks():
    playlist = SpotifyPlaylistMock(["s1", "s2"])

    concatenate = Concatenate([playlist])
    

    assert concatenate.getNextSource() == playlist
    assert concatenate.getNextSource() == playlist
    assert(next(playlist)) == "s1"
    assert concatenate.getNextSource() == playlist
    assert(next(playlist)) == "s2"
    assert concatenate.getNextSource() == playlist

def test_second_source_is_chosen_once_first_is_out_of_tracks():
    playlist1 = SpotifyPlaylistMock(["s1", "s2"])
    playlist2 = SpotifyPlaylistMock(["b1", "b2"])

    concatenate = Concatenate([playlist1, playlist2])

    assert concatenate.getNextSource() == playlist1
    assert(next(playlist1)) == "s1"
    assert concatenate.getNextSource() == playlist1
    assert(next(playlist1)) == "s2"
    assert concatenate.getNextSource() == playlist2

def test_cycles_through_sources_that_are_all_out_of_tracks():
    playlist1 = SpotifyPlaylistMock(["s1"])
    assert(next(playlist1)) == "s1"
    playlist2 = SpotifyPlaylistMock(["b1"])
    assert(next(playlist2)) == "b1"
    playlist3 = SpotifyPlaylistMock(["k1"])
    assert(next(playlist3)) == "k1"

    concatenate = Concatenate([playlist1, playlist2, playlist3])

    assert concatenate.getNextSource() == playlist2
    assert concatenate.getNextSource() == playlist3
    assert concatenate.getNextSource() == playlist1
    assert concatenate.getNextSource() == playlist2
    assert concatenate.getNextSource() == playlist3
    assert concatenate.getNextSource() == playlist1
