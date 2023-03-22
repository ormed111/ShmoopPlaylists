from flask import Flask, request, redirect
from typing import List
import logging
import webbrowser
import threading
import time

from auth import get_auth_url, get_access_token
from generate_playlist import generate_playlist, PLAYLIST_ID

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


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
    logging.debug("Got code from redirect: '%s'", code)
    access_token = get_access_token(code)
    logging.debug("Converted code to access token: '%s'", access_token)
    generated_tracks = generate_playlist(access_token)
    return playlist_desc(generated_tracks)


def open_browser():
    logging.info("Opening browser in 5 seconds")
    time.sleep(5)
    webbrowser.open("http://localhost:1312/")



if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True, port=1312, use_reloader=False)
