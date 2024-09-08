from source.source import Source
from source.outOfTracks import OutOfTracks
from track import Track

class RecentlyPlayed(Source):
    """Provides an iterator to the ids of the last 50 tracks which were recently played by a user.
    """

    def __init__(self, authentication: object):
        self.auth = authentication
        self.tracks = []
        self.nextTrack = 0
        self.response = None

    def _getMoreTracks(self):
        if self.response is None:
            # Request for the first time
            self.response = self.auth.current_user_recently_played()   
        else:
            if self.response and self.response["next"]:
                # Request again
                self.response = self.auth.next(self.response)
            else:
                return False

        if self.response:
            self.tracks += [Track(self.auth, item["track"]) for item in self.response["items"] if item["track"]["id"] is not None]
            return True
        
        return False


    def __iter__(self):
        return self

    def __next__(self):
        self.nextTrack += 1

        if self.nextTrack >= len(self.tracks):
            if not self._getMoreTracks():
                raise OutOfTracks()

        if self.nextTrack < len(self.tracks):
            return self.tracks[self.nextTrack - 1]
        else:
            raise OutOfTracks()

    def __str__(self):
        return "Recently Played"
    
    def __contains__(self, track):
        # get all tracks of the playlist
        while self._getMoreTracks():
            pass

        return track in self.tracks

