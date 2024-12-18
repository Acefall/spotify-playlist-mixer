from spotify_playlist_mixer.source.spotifyPlaylist import SpotifyPlaylist
from spotify_playlist_mixer.source.concatenate import Concatenate

class Deserializer():
    @classmethod
    def fromDict(cls, data):
        class_map = {
            'SpotifyPlaylist': SpotifyPlaylist,
            'Concatenate': Concatenate
            }
        if data['type'] in class_map:
            return class_map[data['type']].fromDict(data)
        else:
            raise ValueError(f"Unknown type: {data['type']}")
