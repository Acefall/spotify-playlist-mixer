from spotify_playlist_mixer.source.source import Source
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.endOfPattern import EndOfPattern

class TakeN(Source):
    def __init__(self, n, source):
        self.n = n
        self.numberOfProvidedTracks = 0
        self.source = source

    def __iter__(self):
        return self
  
    def __next__(self):
        if not self.has_next():
            raise EndOfPattern()
        
        nextValue = next(self.source)

        self.numberOfProvidedTracks += 1
        return nextValue

    def has_next(self):
        return self.numberOfProvidedTracks < self.n

    def reset_pattern(self):
        self.numberOfProvidedTracks = 0
        self.source.reset_pattern()

    def __str__(self):
        return "n: " + str(self.n) + ", numberOfProvidedTracks: " + str(self.numberOfProvidedTracks) + ", source: " + str(self.source)
