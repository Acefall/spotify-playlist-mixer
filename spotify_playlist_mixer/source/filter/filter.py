from spotify_playlist_mixer.source.source import Source

class Filter(Source):
    def __init__(self, source):
        self.source = source

    def __iter__(self):
        return self

    def reset_pattern(self):
        self.source.reset_pattern()