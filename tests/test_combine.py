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

