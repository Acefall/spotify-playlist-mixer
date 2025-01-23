from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.filter.distinctFilterSet import DistinctFilterSet
from spotify_playlist_mixer.source.filter.filter import Filter

class DistinctFilter(Filter):
    def __init__(self, source, observedTracks=None):
        super().__init__(source)
        if observedTracks is None:
            self.observedTracks = DistinctFilterSet()
        else:
            self.observedTracks = observedTracks

    def __next__(self):
        for track in self.source:
            alreadyObserved = track in self.observedTracks
            self.observedTracks.add(track)

            if not alreadyObserved:
                return track
        raise OutOfTracks
    
    def serialize(self, serializer):
        return {
            "source": serializer.serialize(self.source),
            "observedTracks": serializer.serialize(self.observedTracks)
        }

    @classmethod
    def deserialize(cls, data, deserializer):
        return cls(deserializer.deserialize(data["source"]), deserializer.deserialize(data["observedTracks"]))
    