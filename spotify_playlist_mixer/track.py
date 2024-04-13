import spotipy
from spotify_playlist_mixer.audioFeatures import AudioFeatures

class Track:
    def __init__(self, auth, data):
        self.auth = auth
        self.id = data.get("id")
        self.name = data.get("name")
        self.duration_ms = data.get("duration_ms")
        self.popularity = data.get("popularity")
        self.explicit = data.get("explicit")
        self.audio_features = None

    def get_audio_features(self):
        if self.audio_features is None:
            features = self.auth.audio_features(self.id)

            if features:
                self.audio_features = AudioFeatures(features[0])
            else:
                self.audio_features = AudioFeatures({})

        return self.audio_features
    
    def has_attribute(self, attribute):
        if hasattr(self, attribute):
            return True
        else:
            self.get_audio_features()
            return not self.audio_features is None and hasattr(self.audio_features, attribute)
    
    def get_attribute(self, attribute):
        if hasattr(self, attribute):
            return getattr(self, attribute)
        else:
            self.get_audio_features()
            if self.audio_features is None or not hasattr(self.audio_features, attribute):
                return None
            else:
                return getattr(self.audio_features, attribute)

    def __str__(self):
        return f"Track {self.id} \n" \
            f"{self.name}\n" \
            f"Duration: {str(self.duration_ms / 1000)}s\n" \
            f"Popularity: {str(self.popularity)}\n" \
            f"Explicit: {str(self.explicit)}\n" \
            f"=== Audio Features ===\n" \
            f"{str(self.audio_features)}"

