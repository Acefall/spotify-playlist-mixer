class AudioFeatures:
    def __init__(self, data):
        self.acousticness = data.get("acousticness")
        self.danceability = data.get("danceability")
        self.energy = data.get("energy")
        self.instrumentalness = data.get("instrumentalness")
        self.key = data.get("key")
        self.liveness = data.get("liveness")
        self.loudness = data.get("loudness")
        self.mode = data.get("mode")
        self.speechiness = data.get("speechiness")
        self.tempo = data.get("tempo")
        self.time_signature = data.get("time_signature")
        self.valence = data.get("valence")

    def __str__(self):
        return f"Acousticness: {str(self.acousticness)}\n" \
        f"Danceability: {str(self.danceability)}\n" \
        f"Energy: {str(self.energy)}\n" \
        f"Instrumentalness: {str(self.instrumentalness)}\n" \
        f"Key: {str(self.key)}\n" \
        f"Liveness: {str(self.liveness)}\n" \
        f"Loudness: {str(self.loudness)}\n" \
        f"Mode: {str(self.mode)}\n" \
        f"Speechiness: {str(self.speechiness)}\n" \
        f"Tempo: {str(self.tempo)}\n" \
        f"Time Signature: {str(self.time_signature)}\n" \
        f"Valence: {str(self.valence)}\n" \
