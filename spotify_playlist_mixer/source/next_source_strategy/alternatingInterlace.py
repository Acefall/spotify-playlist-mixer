from spotify_playlist_mixer.source.next_source_strategy.nextSourceStrategy import NextSourceStrategy

class AlternatingInterlace(NextSourceStrategy):
    """Chooses the next source. If the current source is the last source, chooses the first source.
    """
    def __init__(self, sources):
        self.sources = sources
        self.currentSource = -1

    def getNextSource(self):
        self.currentSource = (self.currentSource + 1) % len(self.sources)
        return self.sources[self.currentSource]