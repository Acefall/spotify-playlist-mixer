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

    def toDict(self):
        return {
            "type": self.__class__.__name__,
            "source": self.source.toDict()
        }
    
    @classmethod
    def fromDict(cls, data, deserializer):
        return cls(deserializer.fromDict(data["source"]))
