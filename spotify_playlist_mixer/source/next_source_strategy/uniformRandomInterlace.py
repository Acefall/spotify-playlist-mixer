from spotify_playlist_mixer.source.next_source_strategy.nextSourceStrategy import NextSourceStrategy
import random

class UniformRandomInterlace(NextSourceStrategy):
    """Chooses the next source uniformly at random.
    """
    def __init__(self, sources):
        self.sources = sources

    def getNextSource(self):
        return self.sources[random.randint(0, len(self.sources)-1)]