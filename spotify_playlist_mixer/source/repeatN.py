from spotify_playlist_mixer.source.endOfPattern import EndOfPattern
from spotify_playlist_mixer.source.source import Source


class RepeatN(Source):

    def __init__(self, n, source):
        self.n = n
        self.source = source
        self.iterations = 0

    def __iter__(self):
        return self

    def __next__(self):
        print("n:", self.n)
        print("iterations:", self.iterations)
        while self.iterations < self.n:
            try:
                return next(self.source)
            except EndOfPattern:
                self.iterations += 1
                self.source.reset_pattern()
        raise EndOfPattern

    def reset_pattern(self):
        self.iterations = 0
        self.source.reset_pattern()
