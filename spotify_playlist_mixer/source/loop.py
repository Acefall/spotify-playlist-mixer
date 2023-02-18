from spotify_playlist_mixer.source.endOfPattern import EndOfPattern
from spotify_playlist_mixer.source.source import Source


class Loop(Source):

    def __init__(self, source):
        self.source = source

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.source)
        except EndOfPattern:
            self.source.reset_pattern()
            return next(self.source)

    def reset_pattern(self):
        self.source.reset_pattern()
