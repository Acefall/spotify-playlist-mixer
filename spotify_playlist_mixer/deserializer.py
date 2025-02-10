from spotify_playlist_mixer.source.spotifyPlaylist import SpotifyPlaylist
from spotify_playlist_mixer.source.concatenate import Concatenate
from spotify_playlist_mixer.source.loop import Loop
from spotify_playlist_mixer.source.recentlyPlayed import RecentlyPlayed
from spotify_playlist_mixer.source.repeatN import RepeatN
from spotify_playlist_mixer.source.setMinus import SetMinus
from spotify_playlist_mixer.source.takeN import TakeN
from spotify_playlist_mixer.source.shuffle import Shuffle
from spotify_playlist_mixer.source.filter.numericRangeFilter import NumericRangeFilter
from spotify_playlist_mixer.source.filter.equalityFilter import EqualityFilter
from spotify_playlist_mixer.source.filter.distinctFilter import DistinctFilter
from spotify_playlist_mixer.source.filter.distinctFilterSet import DistinctFilterSet
import random


class Deserializer():
    class_map = {
        'Concatenate': Concatenate,
        'Shuffle': Shuffle,
        'Loop': Loop,
        'RecentlyPlayed': RecentlyPlayed,
        'RepeatN': RepeatN,
        'SetMinus': SetMinus,
        'SpotifyPlaylist': SpotifyPlaylist,
        'TakeN': TakeN,
        'NumericRangeFilter': NumericRangeFilter,
        "EqualityFilter": EqualityFilter,
        "DistinctFilter": DistinctFilter,
        "DistinctFilterSet": DistinctFilterSet,
    }

    def __init__(self, auth=None, sourceOfRandomness=random):
        self.auth = auth
        self.sourceOfRandomness = sourceOfRandomness
        self.deserializedObjects = dict()

    def _findChildObjectById(self, root, id):
        child = None
        
        if isinstance(root, list):
            for item in root:
                child = self._findChildObjectById(item, id)
                if child is not None:
                    return child

        if not isinstance(root, dict):
            return None

        if "id" not in root or "data" not in root:
            return None
        
        if root["id"] == id: # Found item
            return root
        
        for _, attributeValue in root["data"]:
            child = self._findChildObjectById(attributeValue, id)
            if child is not None:
                return child
            
        return child

    def deserialize(self, objectDict, root=None):
        if root is None:
            root = objectDict

        # if the id is already in the deserialized objects return immediately
        if objectDict["id"] in self.deserializedObjects:
            return self.deserializedObjects[objectDict["id"]]
        
        # Only id is provided. Full definition of the object must be somewhere in the tree
        if not "type" in objectDict:
            return self.deserialize(self._findChildObjectById(root, objectDict["id"]), root)
        
        if objectDict['type'] in Deserializer.class_map:
            deserializedObject = Deserializer.class_map[objectDict['type']].deserialize(objectDict["data"], self)
            self.deserializedObjects[objectDict['id']] = deserializedObject
            return deserializedObject
        else:
            raise ValueError(f"Unknown type: {objectDict['type']}")
