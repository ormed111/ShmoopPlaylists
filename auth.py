import base64
import os
import requests
from urllib.parse import urlencode


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:1312/callback"

def get_auth_url() -> str:
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "playlist-modify-public"  # space separated
    }
    return "https://accounts.spotify.com/authorize?" + urlencode(params)


def client_auth_string() -> str:
    return base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode('ascii')).decode('ascii')

def get_access_token(code: str) -> str:
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {client_auth_string()}"}
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()

    return response.json()["access_token"]
