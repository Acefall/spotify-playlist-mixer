class DistinctFilter():
    def __init__(self):
        self.observedTracks = set()

    def filter(self, track):
        alreadyObserved = track not in self.observedTracks
        self.observedTracks.add(track)
        return alreadyObserved