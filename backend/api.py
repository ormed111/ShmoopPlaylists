import requests
import json
from typing import List, Optional, Dict, Any, Union
from urllib3.util import Url
import logging

from structs import Album, Track, AlbumImage, SpotifyUser

RequestsMethod = Union[requests.get, requests.post, requests.delete]
    
    
def raise_for_status(response: requests.Response):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        exception_type = type(e)
        raise exception_type(f"{e}. Message: '{response.text}'")

class SpotifyRequest:
    @staticmethod
    def _request(method: RequestsMethod, route: str, access_token: str, **kwargs):
        url = Url(scheme="https", host="api.spotify.com/v1", path=route)
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        logging.debug(f"Request to '{url.url}', headers={headers}, kwargs={kwargs}")
        response = method(url=url.url, headers=headers, **kwargs)
        raise_for_status(response)
        return response.json()

    @classmethod
    def get(cls, route: str, access_token: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = params if params is not None else {}
        return cls._request(method=requests.get, route=route, access_token=access_token, params=params)

    @classmethod
    def post(cls, route: str, access_token: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        data = data if data is not None else {}
        return cls._request(method=requests.post, route=route, access_token=access_token, data=json.dumps(data))

    @classmethod
    def delete(cls, route: str, access_token: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        data = data if data is not None else {}
        return cls._request(method=requests.delete, route=route, access_token=access_token, data=json.dumps(data))


class SpotifyClient:
    def __init__(self, access_token: str):
        self.__access_token = access_token

    def sanity(self):
        # Just a function to check that the client was initialized properly with right auth
        return self.user_info()

    def user_info(self) -> SpotifyUser:
        route = "me"
        data = SpotifyRequest.get(access_token=self.__access_token, route=route)
        logging.info(data)
        return {
            "name": data['display_name'],
            "image": data['images'][0]['url']
        }

    def get_album_id(self, album: Album) -> str:
        route = "search"
        params = {
            "q": f"{album.name.capitalize()} {album.artist.title()}",
            "type": "album",
            "limit": 10
        }
        data = SpotifyRequest.get(access_token=self.__access_token, route=route, params=params)

        # Find the right album in results, to prevent false album ids
        for item in data['albums']['items']:
            if item['name'].lower() != album.name.lower():
                continue
            artists = set([a['name'].lower() for a in item['artists']])
            if album.artist.lower() not in artists:
                continue
            return item['id']

        raise RuntimeError("Failed to find album [%s]", album)

    def get_album_tracks(self, album_id: str) -> List[Track]:
        route = f"albums/{album_id}/tracks"
        data = SpotifyRequest.get(access_token=self.__access_token, route=route)
        return [Track(name=item['name'], id=item['id']) for item in data['items']]
    
    def _get_album(self, album_id: str):
        # Return the full Spotify album object
        route = f"albums/{album_id}"
        return SpotifyRequest.get(access_token=self.__access_token, route=route)

    def get_album_image(self, album_id: str) -> AlbumImage:
        album = self._get_album(album_id=album_id)
        if 'images' in album:        
            return album['images'][0]
        return {}

    def get_album_total_tracks(self, album_id: str) -> int:
        album = self._get_album(album_id=album_id)
        return album.get('total_tracks', 0)

    def get_playlist_tracks(self, playlist_id: str) -> List[Track]:
        route = f"playlists/{playlist_id}/tracks"
        data = SpotifyRequest.get(access_token=self.__access_token, route=route)
        return [Track(name=item['track']['name'], id=item['track']['id']) for item in data['items']]

    def populate_playlist(self, playlist_id: str, tracks: List[Track]):
        route = f"playlists/{playlist_id}/tracks"
        # Only add tracks that don't already exist in the playlist, to prevent duplicates
        existing_tracks = set(self.get_playlist_tracks(playlist_id=playlist_id))
        tracks_to_add = [track for track in tracks if track not in existing_tracks]
        if not tracks_to_add:
            print("All requested tracks already exist")
            return
        data = {"uris": [f"spotify:track:{track.id}" for track in tracks_to_add]}
        SpotifyRequest.post(access_token=self.__access_token, route=route, data=data)

    def clear_playlist(self, playlist_id: str):
        route = f"playlists/{playlist_id}/tracks"
        data = {"uris": [f"spotify:track:{track.id}" for track in self.get_playlist_tracks(playlist_id)]}
        SpotifyRequest.delete(access_token=self.__access_token, route=route, data=data)
