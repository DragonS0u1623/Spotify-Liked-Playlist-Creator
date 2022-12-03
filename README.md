# Spotify Playlist Creator

This is a tool for creating a shareable playlist of your liked songs on Spotify

## Installation

Clone the repository to your local machine and run `pip install Flask Flask-Session spotipy` to install the necessary dependencies. Replace the `ClientID` and `ClientSecret` variables in index.py with your own client ID and Secret from Spotify Developer portal, and add `http://127.0.0.1:8080` to the redirect URI.

## Usage

To use the tool, run `python index.py` in the terminal and go to http://127.0.0.1:8080 and login to Spotify. From there click the link "Create Playlist" and you're done. You'll be automatically redirected to your new playlist when it's finished adding all the songs. (May take a little while depending on how many songs you have liked)
