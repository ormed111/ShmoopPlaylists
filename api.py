import requests
import json
from typing import List, NamedTuple, Optional, Dict, Any, Union
from urllib3.util import Url

RequestsMethod = Union[requests.get, requests.post, requests.delete]

class Album(NamedTuple):
    name: str
    artist: str


class Track(NamedTuple):
    name: str
    id: str


class SpotifyRequest:
    @staticmethod
    def _request(method: RequestsMethod, route: str, access_token: str, **kwargs):
        url = Url(scheme="https", host="api.spotify.com/v1", path=route)
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        response = method(url=url.url, headers=headers, **kwargs)
        response.raise_for_status()
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

    def get_album_tracks(self, album: Album) -> List[Track]:
        album_id = self.get_album_id(album)
        route = f"albums/{album_id}/tracks"
        data = SpotifyRequest.get(access_token=self.__access_token, route=route)
        return [Track(name=item['name'], id=item['id']) for item in data['items']]

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



def get_access_token(client_id, client_secret):
    # Set the token route URL
    url = "https://accounts.spotify.com/api/token"

    # Set the authorization header with the client ID and client secret
    headers = {
        "Authorization": "Basic your_client_id_and_client_secret_here"
    }

    # Set the request body with the authorization code and redirect URI
    data = {
        "grant_type": "authorization_code",
        "code": "your_authorization_code_here",
        "redirect_uri": "your_redirect_uri_here"
    }

    # Make the HTTP request to the Spotify API to get the access token
    response = requests.post(url, headers=headers, data=data)

    # If the request was successful, parse the JSON response and extract the access token
    if response.status_code == 200:
        access_token = response.json()['access_token']
        print(access_token)

    # If the request was not successful, print the error message
    else:
        print(f"Error: {response.text}")

