class DistinctFilterSet():
    def __init__(self):
        self.observedTracks = set()

    def __contains__(self, track):
        return track in self.observedTracks
    
    def add(self, track):
        self.observedTracks.add(track)

    def serialize(self, serializer):
        return {}
    
    @classmethod
    def deserialize(cls, data, deserializer):
        return cls()