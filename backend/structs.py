from typing import TypedDict, NamedTuple

class Album(NamedTuple):
    name: str
    artist: str


class Track(NamedTuple):
    name: str
    id: str


class AlbumJson(TypedDict):
    name: str
    artist: str
    count: int


class AlbumImage(TypedDict):
    url: str
    height: int
    width: int


class SpotifyUser(TypedDict):
    name: str
    image: str
