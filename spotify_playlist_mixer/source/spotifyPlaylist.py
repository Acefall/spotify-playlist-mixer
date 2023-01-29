from source.source import Source
from source.outOfTracks import OutOfTracks


class SpotifyPlaylist(Source):
    """Provides an iterator to the ids of the tracks in a spotify playlist.
    """

    def __init__(self, authentication: object, url=""):
        self.url = url
        self.auth = authentication
        self._queryTracks()
        self.nextTrack = 0

    def _queryTracks(self):
        self.tracks = []

        tracks = self.auth.playlist_tracks(self._getId())
        while tracks:
            self.tracks += [item["track"]["id"] for item in tracks["items"] if item["track"]["id"] is not None]
            if tracks['next']:
                tracks = self.auth.next(tracks)
            else:
                tracks = None

    def _getId(self):
        parts = self.url.split("/")
        idParts = parts[-1].split("?")
        return idParts[0]

    def __iter__(self):
        return self

    def __next__(self):
        if not self.has_next():
            raise OutOfTracks()

        self.nextTrack += 1
        return self.tracks[self.nextTrack - 1]

    def has_next(self):
        return self.nextTrack < len(self.tracks)

    def reset_pattern(self, depp=False):
        self.nextTrack = 0
