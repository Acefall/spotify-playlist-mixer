import random

class Playlist:
    """Provides an iterator to the ids of the tracks in a spotify playlist.
    """

    def __init__(self, authentication: object, url: str, randomize=False):
        """Creates a new playlist.

        Args:
            authentication (object): The spotipy authentication object
            url (str): Url to the playlist
            randomize (bool): True if source should be in a random order
        """
        self.auth = authentication
        self.url = url
        self._queryTracks()
        if randomize:
            random.shuffle(self.tracks)
        self.iterator = iter(self.tracks)

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
        return next(self.iterator)
