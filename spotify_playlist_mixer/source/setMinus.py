from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.source import Source
from spotify_playlist_mixer.source.endOfPattern import EndOfPattern


class SetMinus(Source):
    """This class takes tracks from source1 if they are not contained in source2.
    Source2 must implement the __contains__ method.
    """

    def __init__(self, source1, source2):
        self.source1 = source1
        self.source2 = source2

        self.currentSourceIndex = 0

    def __iter__(self):
        return self

    def __next__(self):
        nextTrack = next(self.source1)
        while nextTrack in self.source2:
            nextTrack = next(self.source1)

        return nextTrack

    def reset_pattern(self):
        pass
