from typing import NamedTuple, List
import random
import logging

from api import SpotifyClient, Album, Track


MY_PLAYLIST_ID = "5aV0JRJMZcXHS5dLckCzRT"
PLAYLIST_ID = "4YK6bqZpc8IhNf1coqaw0w"

class PlaylistAlbum(NamedTuple):
    album: Album
    count: int  # how many songs from this album?


# todo: read this from a config file or UI or something #NurveDoThis
PLAYLIST = [
    PlaylistAlbum(album=Album(name='animals as leaders', artist='animals as leaders'), count=2),
    PlaylistAlbum(album=Album(name='the mountain', artist='haken'), count=2),
    PlaylistAlbum(album=Album(name=r'סטטוס', artist='nunu'), count=3),
    PlaylistAlbum(album=Album(name='Butterfly 3000', artist='King gizzard & the lizard wizard'), count=4)
]


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

    for entry in PLAYLIST:
        try:
            album_tracks = choose_random_tracks_from_album(tracks=client.get_album_tracks(entry.album), count=entry.count)
        except RuntimeError:
            logging.exception("Error while handling album %s, skipping it..", entry.album)
            continue
        logging.info("Tracks chosen from %s: %s", entry.album, album_tracks)
        tracks.extend(album_tracks)

    logging.info(f"Adding total of {len(tracks)} tracks to playlist")
    client.clear_playlist(playlist_id=PLAYLIST_ID)
    client.populate_playlist(playlist_id=PLAYLIST_ID, tracks=tracks)
    return [track.name for track in tracks]
