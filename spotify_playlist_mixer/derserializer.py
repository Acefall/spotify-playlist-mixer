from spotify_playlist_mixer.source.spotifyPlaylist import SpotifyPlaylist
from spotify_playlist_mixer.source.concatenate import Concatenate
from spotify_playlist_mixer.source.loop import Loop
from spotify_playlist_mixer.source.recentlyPlayed import RecentlyPlayed
from spotify_playlist_mixer.source.repeatN import RepeatN
from spotify_playlist_mixer.source.setMinus import SetMinus
from spotify_playlist_mixer.source.takeN import TakeN


class Deserializer():
    class_map = {
        'Concatenate': Concatenate,
        'Loop': Loop,
        'RecentlyPlayed': RecentlyPlayed,
        'RepeatN': RepeatN,
        'SetMinus': SetMinus,
        'SpotifyPlaylist': SpotifyPlaylist,
        'TakeN': TakeN
    }

    def __init__(self, serializedObjects, auth=None):
        self.serializedObjects = serializedObjects
        self.deserializedObjects = {}
        self.auth = auth

    def deserialize(self, objectDict):
        # if the id is already in the deserialized objects return immediately
        if objectDict["id"] in self.deserializedObjects:
            return self.deserializedObjects[objectDict["id"]]
        
        # Only id is provided. Full definition of the object must be in serializedObjects
        if not "type" in objectDict:
            return self.deserialize(self.serializedObjects[objectDict["id"]])
        
        if objectDict['type'] in Deserializer.class_map:
            deserializedObject = Deserializer.class_map[objectDict['type']].deserialize(objectDict["data"], self)
            self.deserializedObjects[objectDict['id']] = deserializedObject
            return deserializedObject
        else:
            raise ValueError(f"Unknown type: {objectDict['type']}")
