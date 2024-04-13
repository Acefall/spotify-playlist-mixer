from spotify_playlist_mixer.source.filter.filter import Filter
from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
import math

class BooleanFilter(Filter):
    def __init__(self, source, attribute, requiredBoolean):
        super().__init__(source)
        self.attribute = attribute
        self.requiredBoolean = requiredBoolean

    def __next__(self):
        for track in self.source:
            if track.has_attribute(self.attribute) and track.get_attribute(self.attribute) == self.requiredBoolean:
                return track
        raise OutOfTracks
