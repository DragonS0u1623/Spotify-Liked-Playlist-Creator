import os
from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
auth_manager = spotipy.oauth2.SpotifyOAuth(
        client_id='<your_client_id>',
        client_secret='<your_client_secret>',
        redirect_uri='http://127.0.0.1:8080',
        scope='user-library-read user-library-modify playlist-modify-private playlist-modify-public',
        cache_handler=cache_handler,
        show_dialog=True)

@app.route('/')
def index():
    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 3. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return f'<h2>Hi {spotify.me()["display_name"]}, ' \
           f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
           f'<a href="/create">Create Playlist</a> | ' \



@app.route('/sign_out')
def sign_out():
    session.pop("token_info", None)
    return redirect('/')


def save_playlist(spotify, playlist, songs):
    song_ids = [song['track']['id'] for song in songs['items']]
    spotify.user_playlist_add_tracks(spotify.me()["id"], playlist['id'], song_ids)


@app.route('/create')
def playlists():
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    # Make new playlist
    playlist_name = 'My Favorite Songs'
    playlist = spotify.user_playlist_create(spotify.me()["id"], playlist_name, False, False, '')
    
    # Get liked songs
    songs = spotify.current_user_saved_tracks()
    save_playlist(spotify, playlist, songs)

    while (songs['next']):
        songs = spotify.next(songs)
        save_playlist(spotify, playlist, songs)

    return redirect(playlist["external_urls"]["spotify"])


if __name__ == '__main__':
    app.run(threaded=True, port=8080)