from spotify_playlist_mixer.source.source import Source
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks


class SpotifyPlaylistMock(Source):
    """Mocks the class SpotifyPlaylist
    """

    def __init__(self, trackIds, sourceOfRandomness=None):
        self.nextTrack = 0
        self.tracks = trackIds

        if sourceOfRandomness is not None:
            sourceOfRandomness.shuffle(self.tracks)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.has_next():
            raise OutOfTracks()

        self.nextTrack += 1
        return self.tracks[self.nextTrack - 1]

    def has_next(self):
        return self.nextTrack < len(self.tracks)

    def __str__(self):
        return str(self.tracks)
