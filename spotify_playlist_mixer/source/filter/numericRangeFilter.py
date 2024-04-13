from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.filter.filter import Filter
import math

class NumericRangeFilter(Filter):
    def __init__(self, source, attribute, minAttribute, maxAttribute):
        super().__init__(source)
        self.attribute = attribute
        self.minAttribute = min(minAttribute, maxAttribute)
        self.maxAttribute = max(minAttribute, maxAttribute)

    def __next__(self):
        for track in self.source:
            if track.has_attribute(self.attribute):
                attribute = track.get_attribute(self.attribute)
                if attribute >= self.minAttribute and attribute <= self.maxAttribute:
                    return track
        raise OutOfTracks
