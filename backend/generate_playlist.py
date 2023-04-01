import json
from typing import NamedTuple, List
import random
import logging
from pathlib import Path

from api import SpotifyClient
from structs import AlbumJson, Album, Track

GAYLIST = "7sJdvYeZ7Xe78qXmPOhDQ0"
PLAYLIST_ID = "5aV0JRJMZcXHS5dLckCzRT"
DEFAULT_ALBUMS_JSON = Path(__file__).parent / "albums.json"



class PlaylistAlbum(NamedTuple):
    album: Album
    count: int  # how many songs from this album?

    @classmethod
    def from_json(cls, entry: AlbumJson) -> "PlaylistAlbum":
        album = Album(name=entry["name"], artist=entry["artist"])
        return cls(album=album, count=entry["count"])

    def to_json(self) -> AlbumJson:
        # Maybe we'll use this in the future when we add a user interface for creating the JSON
        return {
            "name": self.album.name,
            "artist": self.album.artist,
            "count": self.count
        }


def read_albums_from_file(path: Path = DEFAULT_ALBUMS_JSON) -> List[PlaylistAlbum]:
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return [PlaylistAlbum.from_json(entry) for entry in data]


def choose_random_tracks_from_album(tracks: List[Track], count: int) -> List[Track]:
    if count > len(tracks):
        raise RuntimeError(f"Error in configuration, asked for {count} tracks from album that contains only {len(tracks)} songs")

    chosen_tracks = []
    while len(chosen_tracks) < count:
        track = random.choice(tracks)
        chosen_tracks.append(track)
        tracks.remove(track)
    return chosen_tracks


def generate_playlist(client: SpotifyClient, albums_path: Path = DEFAULT_ALBUMS_JSON) -> List[str]:
    tracks = []

    playlist_albums = read_albums_from_file(path=albums_path)
    for entry in playlist_albums:
        try:
            album_id = client.get_album_id(album=entry.album)
            album_tracks = choose_random_tracks_from_album(tracks=client.get_album_tracks(album_id),
                                                           count=entry.count)
        except RuntimeError:
            logging.exception("Error while handling album %s, skipping it..", entry.album)
            continue
        logging.info("Tracks chosen from %s: %s", entry.album, album_tracks)
        tracks.extend(album_tracks)

    logging.info(f"Adding total of {len(tracks)} tracks to playlist")
    client.clear_playlist(playlist_id=PLAYLIST_ID)
    client.populate_playlist(playlist_id=PLAYLIST_ID, tracks=tracks)
    return [track.name for track in tracks]
