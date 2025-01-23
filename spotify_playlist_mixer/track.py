import spotipy

class Track:
    def __init__(self, auth, data):
        self.auth = auth
        self.id = data.get("id")
        self.name = data.get("name")
        self.duration_ms = data.get("duration_ms")
        self.popularity = data.get("popularity")
        self.explicit = data.get("explicit")


    def __str__(self):
        return f"Track {self.id} \n" \
            f"{self.name}\n" \
            f"Duration: {str(self.duration_ms / 1000)}s\n" \
            f"Popularity: {str(self.popularity)}\n" \
            f"Explicit: {str(self.explicit)}\n" \
    
    def __eq__(self, other):
        if isinstance(other, Track):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return self.id.__hash__()

