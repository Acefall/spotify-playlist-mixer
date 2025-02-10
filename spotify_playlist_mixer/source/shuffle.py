from spotify_playlist_mixer.source.outOfTracks import OutOfTracks
from spotify_playlist_mixer.source.source import Source

MAX_SHUFFLE_LENGTH = 10000

class Shuffle(Source):
    """This class provides the tracks of the provided source in a random order
    """

    def __init__(self, source, sourceOfRandomness):
        self.source = source
        self.tracks = []
        self.nextTrack = 0
        self.shuffled = False
        self.sourceOfRandomness = sourceOfRandomness

        

    def _shuffle(self):
        for track in self.source:
            self.tracks.append(track)

            # Limit the number of iterations if the source contains a loop
            if len(self.tracks) > MAX_SHUFFLE_LENGTH:
                break

        self.sourceOfRandomness.shuffle(self.tracks)
        self.shuffled = True

    def __iter__(self):
        return self

    def __next__(self):
        if not self.shuffled:
            self._shuffle()

        if self.nextTrack >= len(self.tracks):
            raise OutOfTracks()
        
        track = self.tracks[self.nextTrack]
        self.nextTrack += 1
        return track


    def __contains__(self, track):
        return track in self.tracks

    def reset_pattern(self):
        pass

   
    def serialize(self, serializer):
        return {
            "source": serializer.serialize(self.source)
        }
    
    @classmethod
    def deserialize(cls, data, deserializer):
        return cls(deserializer.deserialize(data["source"]), deserializer.sourceOfRandomness)
    

    
