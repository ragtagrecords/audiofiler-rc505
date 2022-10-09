import requests
from vars import songs, songNames

def getSongs():
    print("getSongs entered")
    # todo: move this request and add some kind of loading screen
    if (requests.get('https://api.ragtagrecords.com/songs')):
        songsDatabase = (requests.get(
        'https://api.ragtagrecords.com/songs')).json()
        print(songsDatabase)
    else: songsDatabase = []

    # song dictionary:
    for song in songsDatabase:
        songObject = {"name": None, "id": None}
        songObject["name"] = song["name"]
        songObject["id"] = song["id"]
        songs.append(songObject)

    for song in songs:
        songNames.append(song["name"])
