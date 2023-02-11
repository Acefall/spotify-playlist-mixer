from spotify_playlist_mixer.source.combine import Combine
from tests.source.spotifyPlaylistMock import SpotifyPlaylistMock
from spotify_playlist_mixer.source.next_source_strategy.alternatingInterlace import AlternatingInterlace
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.takeN import TakeN
import pytest

# out of tracks is thrown
# cycles through take n

def test_forwards_out_of_tracks():
    playlist1 = TakeN(1, SpotifyPlaylistMock([1, 2]))
    playlist2 = TakeN(1,SpotifyPlaylistMock([3, 4, 5, 6, 7]))


    nextSourceStrategy = AlternatingInterlace([playlist1, playlist2])
    combine = Combine([playlist1, playlist2], nextSourceStrategy)

    assert next(combine) == 1
    assert next(combine) == 3
    assert next(combine) == 2
    assert next(combine) == 4

    with pytest.raises(OutOfTracks) as e_info:
        next(combine)

    with pytest.raises(OutOfTracks) as e_info:
        next(combine)


def test_complex_combination_of_take_n():
    source1 = TakeN(3, SpotifyPlaylistMock([11, 12, 13, 14, 15, 16, 17, 18, 19]))
    source2 = TakeN(2, SpotifyPlaylistMock([21, 22, 23, 24, 25, 26, 27]))
    source3 = TakeN(1, SpotifyPlaylistMock([31, 32, 33]))

    sourcesCombine1 = [source1, source2]
    interlace1 = AlternatingInterlace(sourcesCombine1)
    combine1 = Combine(sourcesCombine1, interlace1)

    rootSources = [combine1, source3]
    rootInterlace = AlternatingInterlace(rootSources)

    playlist = Combine(rootSources, rootInterlace)

    assert next(playlist) == 11
    assert next(playlist) == 12
    assert next(playlist) == 13
    assert next(playlist) == 21
    assert next(playlist) == 22
    assert next(playlist) == 31
    assert next(playlist) == 14
    assert next(playlist) == 15
    assert next(playlist) == 16
    assert next(playlist) == 23
    assert next(playlist) == 24
    assert next(playlist) == 32
