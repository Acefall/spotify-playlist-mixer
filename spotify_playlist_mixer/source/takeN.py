from spotify_playlist_mixer.source.source import Source
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks

class TakeN(Source):
    def __init__(self, n, source):
        self.n = n
        self.numberOfProvidedTracks = 0
        self.source = source

    def __iter__(self):
        return self
  
    def __next__(self):
        if not self.has_next():
            raise OutOfTracks()
        
        if self.numberOfProvidedTracks >= self.n:
            print("take N raises stopiteration")
            raise StopIteration()

        self.numberOfProvidedTracks += 1
        return next(self.source)

    def has_next(self):
        return self.source.has_next()

    def reset_pattern(self, deep=False):
        self.numberOfProvidedTracks = 0
        if deep:
            self.source.reset_pattern(deep)

    def __str__(self):
        return "n: " + str(self.n) + ", numberOfProvidedTracks: " + str(self.numberOfProvidedTracks) + ", source: " + str(self.source)
