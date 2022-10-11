from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth , SpotifyClientCredentials
import requests
#Billboard Music scraping data section
URL = "https://www.billboard.com/charts/hot-100/#"
URL2="https://www.billboard.com/charts/hot-100/2000-08-12/"
response = requests.get(url=URL)
music_data = response.text
soup = BeautifulSoup(music_data,"html.parser")
test_data = soup.find_all(name="h3", class_="c-title", id="title-of-a-story")
list = []
for i in test_data:
    list.append(i.get_text())

list_2 = [x.replace('\t','').replace('\n','') for x in list]
test = []
for i in range(len(list_2[9:])):
    if i%2==0 and list_2[i]!="Producer(s):":
        test.append(list_2[i])

music = test[3:103]
print(music)
#file section in music scarping data
with open("music_name","w") as file2:
    for i in music:
        file2.write(f"{i}\n")

# Spotify section:
app_key = "your own client key"
client_secret = "your own client secret key"
#authorization to spotify
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               client_id=app_key,
                                               client_secret=client_secret,
                                               redirect_uri="http://example.com"))


year_want = input("what is the year you want(yyy-mmm-dd): ")
year = year_want.split("-")[0]
curren_useerrr = sp.current_user()
# print(f"{curren_useerrr['display_name']}:{curren_useerrr['id']}")
##searching list:
list_uris = []
for song in music:
    result2 = sp.search(q = f"track:{song} year:{year}", type="track")
    try:
        uri = result2['tracks']['items'][0]['uri']
        list_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist ")
    # print(f"name:{result2['tracks']['items'][0]['album']['artists'][0]['name']}, {result2['tracks']['items'][0]['album']['artists'][0]['uri']}")
playlists = sp.user_playlist_create(user=curren_useerrr['id'],name = "100 billboards", public=False)
print(playlists)
print(len(list_uris))
print(len(music))
sp.playlist_add_items(playlist_id=playlists["id"],items=list_uris,position=None)
