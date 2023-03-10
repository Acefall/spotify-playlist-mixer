from source.source import Source

class SpotifyPlaylistMixer:
    """Provides functionality to create a new playlist from a source that provides tracks.
    """

    def __init__(self, authorization, spotifyId):
        self.auth = authorization
        self.spotifyId = spotifyId

    def create(self, name: str, playlist: Source):
        """Creates a new spotify playlist based on the given playlist.

        Args:
            playlistName (string): The name of the new playlist
            playlist (Source): The source for the tracks
        """
        
        trackIds = []
        for track in playlist:
            trackIds.append(track.id)

        newPlaylist = self.auth.user_playlist_create(self.spotifyId, name)
        for i in range(0, len(trackIds), 100):
            self.auth.user_playlist_add_tracks(
                self.spotifyId, newPlaylist["id"], trackIds[i:i+100])
