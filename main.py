from typing import NamedTuple
import random

from api import SpotifyClient, Album


PLAYLIST_ID = "5aV0JRJMZcXHS5dLckCzRT"


class PlaylistAlbum(NamedTuple):
    album: Album
    count: int


PLAYLIST = [
    PlaylistAlbum(album=Album(name='animals as leaders', artist='animals as leaders'), count=2),
    PlaylistAlbum(album=Album(name='the mountain', artist='haken'), count=2),
    PlaylistAlbum(album=Album(name=r'סטטוס', artist='nunu'), count=3)
]

def generate_playlist():
    tracks = []
    client = SpotifyClient(access_token=ACCESS_TOKEN)

    for entry in PLAYLIST:
        album_tracks = random.choices(client.get_album_tracks(entry.album), k=entry.count)
        tracks.extend(album_tracks)

    print(f"Adding total of {len(tracks)} tracks to playlist")
    client.clear_playlist(playlist_id=PLAYLIST_ID)
    client.populate_playlist(playlist_id=PLAYLIST_ID, tracks=tracks)

if __name__ == '__main__':
    generate_playlist()
