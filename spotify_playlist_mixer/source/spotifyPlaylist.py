from source.source import Source
from source.outOfTracks import OutOfTracks


class SpotifyPlaylist(Source):
    """Provides an iterator to the ids of the tracks in a spotify playlist.
    """

    def __init__(self, authentication: object, url=""):
        self.url = url
        self.auth = authentication
        self.tracks = []
        self.nextTrack = 0
        self.response = None

    def _getMoreTracks(self):
        if self.response is None:
            # Request for the first time
            self.response = self.auth.playlist_tracks(self._getId())   
        else:
            if self.response and self.response["next"]:
                # Request again
                self.response = self.auth.next(self.response)
            else:
                return False

        if self.response:
            self.tracks += [item["track"]["id"] for item in self.response["items"] if item["track"]["id"] is not None]
            return True
        
        return False



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

        if self.nextTrack >= len(self.tracks):
            if not self._getMoreTracks():
                raise OutOfTracks()

        if self.nextTrack < len(self.tracks):
            return self.tracks[self.nextTrack - 1]
        else:
            raise OutOfTracks()

    def has_next(self):
        return self.nextTrack < len(self.tracks) or self._getMoreTracks()

    def __str__(self):
        return self.url
