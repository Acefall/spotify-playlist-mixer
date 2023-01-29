from spotify_playlist_mixer.source.source import Source
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks

class Combine(Source):
    def __init__(self, sources, nextSourceStrategy):
        self.sources = sources
        if len(sources) == 0:
            raise ValueError("The list of sources must not be empty.")
        self.currentSource = self.sources[0]
        self.nextSourceStrategy = nextSourceStrategy


    def __iter__(self):
        return self

    def __next__(self):
        if not self.has_next():
            raise OutOfTracks()

        nextValue = None
        while True: 
            try:
                nextValue = next(self.currentSource)
                break
            except OutOfTracks as e:
                raise e
            except StopIteration:
                self.currentSource.reset_pattern()
                self.currentSource = self.nextSourceStrategy.getNextSource()

        return nextValue
        

    def has_next(self):
        return self.currentSource.has_next()

    def reset_pattern(self, deep=False):
        for source in self.sources:
            source.reset_pattern(deep)