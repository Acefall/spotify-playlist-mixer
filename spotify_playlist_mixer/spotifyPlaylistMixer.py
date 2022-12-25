class SpotifyPlaylistMixer:
    """Provides functionality to mix several spotify playlists
    into one based on a given pattern.
    """

    def __init__(self, authorization, spotifyId):
        self.auth = authorization
        self.spotifyId = spotifyId

    def _build_track_list_from_pattern(
            self,
            playlist: dict,
            pattern: object
    ):
        """Mixes the ids of the given playlistst into a new list
        based on pattern.

        Args:
            playlists (dict): Dictionary of playlists
            identified by their pattern key
            pattern (object): Iterator that provides
            keys that identify playlists

        Returns:
            list: List of mixed track ids
        """
        ids = []
        for key in pattern:
            try:
                ids.append(next(playlist[key]))
            except StopIteration as stopIteration:
                break

        return ids

    def mix(self, playlistName: str, playlists: dict, pattern: object):
        """Creates a new playlist which is a mix of the given playlists
        based on the given pattern.

        Args:
            playlistName (string): The name of the new playlist
            playlists (dict): Dictionary of playlists
            identified by their pattern key
            pattern (object): Iterator that provides keys
            that identify playlists
        """
        mixedTracks = self._build_track_list_from_pattern(playlists, pattern)

        newPlaylist = self.auth.user_playlist_create(
            self.spotifyId, playlistName)
        for i in range(0, len(mixedTracks), 100):
            self.auth.user_playlist_add_tracks(
                self.spotifyId, newPlaylist["id"], mixedTracks[i:i+100])
