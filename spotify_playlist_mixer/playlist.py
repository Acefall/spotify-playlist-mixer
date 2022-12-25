class Playlist:
    """Provides an iterator to the ids of t he tracsk in a spotify playlist.
    """

    def __init__(self, authentication: object, url: str):
        """Creates a new playlist.

        Args:
            authentication (object): The spotipy authentication object
            url (str): Url to the playlist
        """
        self.auth = authentication
        self.url = url
        self._queryTracks()
        self.iterator = iter(self.tracks)

    def _queryTracks(self):
        self.tracks = []

        tracks = self.auth.playlist_tracks(self._getId())
        while tracks:
            self.tracks += [item["track"]["id"] for item in tracks["items"]]
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
