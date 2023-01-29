from spotify_playlist_mixer.source.next_source_strategy.nextSourceStrategy import NextSourceStrategy

class Concatenate(NextSourceStrategy):
    """
    Chooses the next source if the current source does not have a next element.
    If the current source is the last source, chooses the first source.
    """

    def __init__(self, sources):
        self.sources = sources
        self.currentSource = 0

    def getNextSource(self):
        if not self.sources[self.currentSource].has_next():
            self.currentSource = (self.currentSource + 1) % len(self.sources)
        return self.sources[self.currentSource]

    