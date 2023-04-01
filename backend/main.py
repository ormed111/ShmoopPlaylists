from flask import Flask, request, redirect
from flask_cors import CORS
from typing import List, Optional
import logging
import webbrowser
import threading
import json
import time

from api import SpotifyClient
from auth import get_auth_url, get_access_token, get_ip, get_port
from generate_playlist import generate_playlist, PLAYLIST_ID, DEFAULT_ALBUMS_JSON, PlaylistAlbum

app = Flask(__name__)
CORS(app)


class GlobalAppContext:
    def __init__(self):
        self.client: Optional[SpotifyClient] = None


logging.basicConfig(level=logging.DEBUG)

ctx = GlobalAppContext()


@app.route("/")
def home():
    auth = get_auth_url()
    logging.debug("Redirecting client to '%s'", auth)
    return redirect(auth)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    logging.debug("Got code from redirect: '%s'", code)
    access_token = get_access_token(code)
    logging.debug("Converted code to access token: '%s'", access_token)

    ctx.client = SpotifyClient(access_token=access_token)
    ctx.client.sanity()

    logging.info("Authorization successful")

    return redirect("/to_frontend")


@app.route("/to_frontend")
def frontend():
    # todo: this shouldn't be hardcoded
    fe = "http://localhost:8080"
    logging.debug("redirecting to frontend: '%s'", fe)
    return redirect(fe)


@app.route("/user_info")
def user_info():
    data = ctx.client.sanity()
    user_dict = {
        "name": data['display_name'],
        "image": data['images'][0]['url']
    }
    return user_dict, 200


def playlist_desc(tracks: List[str]) -> str:
    playlist_link = f'<a href="https://open.spotify.com/playlist/{PLAYLIST_ID}">playlist</a>'
    desc = f"Generated {playlist_link} ({len(tracks)} tracks):<br>"
    for i, track in enumerate(tracks):
        desc += f"{i+1}. {track}<br>"
    return desc


@app.route("/generate")
def generate():
    generated_tracks = generate_playlist(client=ctx.client)
    return playlist_desc(generated_tracks)


@app.route("/albums")
def albums():
    # todo: refactor this when I decide on the final JSON format
    with DEFAULT_ALBUMS_JSON.open('r', encoding='utf-8') as f:
        playlist_albums = json.load(f)
    if 'id' in playlist_albums[0]:
        # Already enriched
        return playlist_albums
    # Need to enrich albums json
    for album in playlist_albums:
        album['id'] = ctx.client.get_album_id(PlaylistAlbum.from_json(album).album)
        album['image'] = ctx.client.get_album_image(album['id'])
        album['total_tracks'] = ctx.client.get_album_total_tracks(album['id'])
    with DEFAULT_ALBUMS_JSON.open('w', encoding='utf-8') as f:
        json.dump(playlist_albums, f, indent=4)
    return playlist_albums


def open_browser():
    logging.info("Opening browser in 5 seconds")
    time.sleep(5)
    webbrowser.open(f"http://{get_ip()}:{get_port()}/")



if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True, host=get_ip(), port=get_port(), use_reloader=False)
