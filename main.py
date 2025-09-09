import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_URL = "https://accounts.spotify.com/api/token"
CLIENT_ID = "YOUR_ID"
CLIENT_SECRET = "YOUR_SECRET"
URL = "https://www.billboard.com/charts/hot-100/"
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# Use this to get your Header info, https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending/
headers = {
    "USER-AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/139.0.0.0 Safari/537.36"

}

response = requests.get(URL + date, headers=headers)
top_100_songs = response.text
soup = BeautifulSoup(top_100_songs, "html.parser")
song_titles = soup.select("li ul li h3")
song_list = [song.getText().strip() for song in song_titles]
# print(song_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://127.0.0.1:3000",
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt",
        username="YOUR_USERNAME")
)

user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
