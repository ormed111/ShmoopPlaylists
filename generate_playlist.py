from typing import NamedTuple, List
import random
import logging

from api import SpotifyClient, Album, Track

GAYLIST = "7sJdvYeZ7Xe78qXmPOhDQ0"

PLAYLIST_ID = "5aV0JRJMZcXHS5dLckCzRT"


class PlaylistAlbum(NamedTuple):
    album: Album
    count: int  # how many songs from this album?


def load_albums_from_file(path="albums.json") -> List[PlaylistAlbum]:

    with open(path, "r", encoding='utf-8') as f:
        data = json.load(f)
    return [PlaylistAlbum(album=Album(name=entry["name"], artist=entry["artist"]), count=entry["count"])
            for entry in data]


def choose_random_tracks_from_album(tracks: List[Track], count: int) -> List[Track]:
    if count > len(tracks):
        raise RuntimeError(f"Error in configuration, asked for {count} tracks from album that contains only {len(tracks)} songs")

    chosen_tracks = []
    while len(chosen_tracks) < count:
        track = random.choice(tracks)
        chosen_tracks.append(track)
        tracks.remove(track)
    return chosen_tracks


def generate_playlist(client: SpotifyClient) -> List[str]:
    tracks = []


    from pathlib import Path
    albums_path = Path(__file__).parent / "albums.json"
    playlist = load_albums_from_file(path=albums_path)

    for entry in playlist:
        try:
            album_tracks = choose_random_tracks_from_album(tracks=client.get_album_tracks(entry.album),
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
