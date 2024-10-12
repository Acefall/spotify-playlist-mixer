from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.source import Source
from spotify_playlist_mixer.source.endOfPattern import EndOfPattern


class Concatenate(Source):
    """This class takes tracks from the first playlist until it raises a stop iteration.
    Then it switches to the next palylist until it raises a stop iteration.
    """

    def __init__(self, sources):
        self.sources = sources
        if len(sources) == 0:
            raise ValueError("The list of sources must not be empty.")
        self.currentSourceIndex = 0

    def __iter__(self):
        return self

    def __next__(self):
        for sourceIndex in range(self.currentSourceIndex, len(self.sources)):
            try:
                return next(self.sources[self.currentSourceIndex])
            except OutOfTracks as e:
                raise e
            except EndOfPattern:
                if self.currentSourceIndex >= len(self.sources) - 1:
                    raise EndOfPattern()
                self.currentSourceIndex = sourceIndex + 1

        raise EndOfPattern()

    def reset_pattern(self):
        self.currentSourceIndex = 0
        for source in self.sources:
            source.reset_pattern()
