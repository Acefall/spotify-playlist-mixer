from spotify_playlist_mixer.source.filter.filter import Filter
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks

class EqualityFilter(Filter):
    def __init__(self, source, attribute, expectedValue):
        super().__init__(source)
        self.attribute = attribute
        self.expectedValue = expectedValue

    def __next__(self):
        for track in self.source:
            attributeValue = getattr(track, self.attribute)
            if attributeValue == self.expectedValue:
                return track
        raise OutOfTracks
    
    def serialize(self, serializer):
        return {
            "source": serializer.serialize(self.source),
            "attribute": self.attribute,
            "expectedValue" : self.expectedValue
        }

    @classmethod
    def deserialize(cls, data, deserializer):
        return cls(deserializer.deserialize(data["source"]), data["attribute"], data["expectedValue"])
