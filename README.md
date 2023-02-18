# Spotify Playlist Mixer
This tool mixes spotify playlists for you based on other playlists.

## Installation
1. Install python 3.10 or higher
2. Install poetry with `pip install poetry`
3. Checkout this repo
4. Run `cd spotify-playlist-mixer`
5. Run `poetry install`

## Usage
Adjust the `main.py` file to your needs. Change the `spotifyId` to your spotify id. Add `sources` or modify the existing ones. Also give your new playlist a fancy `newPlaylistName`.

Fill in the secrets in `spotify_playlist_mixer/spotipySecrets.py`. Ask the author of this repo for details.

Then run `poetry run python spotify_playlist_mixer/main.py`. This should open a new browser window. Log into your spotify account.

A new playlist should appear in your spotify profile.