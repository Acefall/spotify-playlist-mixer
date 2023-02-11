from spotify_playlist_mixer.source.source import Source
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks

class Combine(Source):
    def __init__(self, sources, nextSourceStrategy):
        self.sources = sources
        if len(sources) == 0:
            raise ValueError("The list of sources must not be empty.")
        self.nextSourceStrategy = nextSourceStrategy
        self.currentSource = self.nextSourceStrategy.getNextSource()

        # Stores for each source whether it has thrown the out of tracks exception
        self.hasThrownOutOfTracks = {key: value for key, value in [(source, False) for source in self.sources]}


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
                if self.hasThrownOutOfTracks[self.currentSource]:
                    raise e
                self.hasThrownOutOfTracks[self.currentSource] = True
                self.currentSource = self.nextSourceStrategy.getNextSource()
            except StopIteration:
                self.currentSource.reset_pattern()
                self.currentSource = self.nextSourceStrategy.getNextSource()

        return nextValue
        

    def has_next(self):
        for source in self.sources:
            if source.has_next():
                return True
        return False

    def reset_pattern(self, deep=False):
        for source in self.sources:
            source.reset_pattern(deep)