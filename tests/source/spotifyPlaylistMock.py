from spotify_playlist_mixer.source.source import Source
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks


class SpotifyPlaylistMock(Source):
    """Mocks the class SpotifyPlaylist
    """

    def __init__(self, tracks):
        self.nextTrack = 0
        self.tracks = tracks


    def __iter__(self):
        return self

    def __next__(self):
        if self.nextTrack >= len(self.tracks):
            raise OutOfTracks()
        
        track = self.tracks[self.nextTrack]
        self.nextTrack += 1
        return track

    def __str__(self):
        return str(self.tracks)
    
    def __contains__(self, track):
        return track in self.tracks
    
    def serialize(self, serializer):
        return {
            "tracks": self.tracks
        }
    
    @classmethod
    def deserialize(cls, data, deserializer):
        return cls(data["tracks"])
