from flask import Flask, request, redirect
from typing import List
import logging

from auth import get_auth_url, get_access_token
from generate_playlist import generate_playlist, PLAYLIST_ID

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route("/")
def home():
    return redirect(get_auth_url())


def playlist_desc(tracks: List[str]) -> str:
    playlist_link = f'<a href="https://open.spotify.com/playlist/{PLAYLIST_ID}">playlist</a>'
    desc = f"Generated {playlist_link} ({len(tracks)} tracks):<br>"
    for i, track in enumerate(tracks):
        desc += f"{i+1}. {track}<br>"
    return desc


@app.route("/callback")
def callback():
    code = request.args.get("code")
    access_token = get_access_token(code)
    generated_tracks = generate_playlist(access_token)
    return playlist_desc(generated_tracks)


if __name__ == '__main__':
    app.run(debug=True, port=1312)
