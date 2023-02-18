from spotify_playlist_mixer.source.filter.filter import Filter
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
import math

class BooleanFilter(Filter):
    def __init__(self, source, getAttribute, requiredBoolean):
        super().__init__(source)
        self.getAttribute = getAttribute
        self.requiredBoolean = requiredBoolean

    def __next__(self):
        for track in self.source:
            if self.getAttribute(track) == self.requiredBoolean:
                return track
        raise OutOfTracks
