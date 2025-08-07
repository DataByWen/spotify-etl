from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import mysql.connector
from mysql.connector import errorcode
import os 
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

# used for authenticating requests
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

sp = spotipy.Spotify(auth_manager=auth_manager, requests_timeout=20, retries=5)

playlist_url_list = [
    os.getenv("PLAYLIST_1"),
    os.getenv("PLAYLIST_2"),
    os.getenv("PLAYLIST_3")
]

playlist_id_list = []
for url in playlist_url_list:
    playlist_id_list.append(url.split("/")[-1])


# playlist_tracks method returns a paginated result with details of the tracks of a playlist. So you need to iterate over all pages to get the full data 
def get_all_tracks_from_playlist(playlist_id):
    try:
        print("New playlist!")
        tracks_response = sp.playlist_tracks(playlist_id) # returns 1 page of response
        tracks = tracks_response["items"]
        page = 1 # for printing purposes
        print(f"Page {page} fetched for playlist {playlist_id}")
        while tracks_response["next"]:
            tracks_response = sp.next(tracks_response) # move onto the next page
            page += 1
            print(f"Page {page} fetched for playlist {playlist_id}")
            tracks.extend(tracks_response["items"])
        return tracks # an list of items (for 1 playlist)
    except Exception as e:
        print(f"Error fetching playlist {playlist_id}: {e}")
        return []


def get_list_track_details() -> list:
    new_tracks = [] # this stores a list of tracks in the playlist and stores its metadata

    # iterate through all the playlists, then iterate through all the songs
    for playlist_id in playlist_id_list:
        tracks_array = get_all_tracks_from_playlist(playlist_id) 

        for item in tracks_array:
            track = item["track"]
            track_metadata = {
                "playlist_id": playlist_id,
                "playlist_user_id": item["added_by"]["id"],
                "track_added_at": parse_date(item["added_at"]),
                "track_id": track["id"],
                "track_name": track["name"],
                "track_duration_mins": round(track["duration_ms"] / 60000, 2), # convert ms to mins
                "track_uri": track["uri"],
                "popularity": track["popularity"],
                "explicit_track": track["explicit"],
                "album_id": track["album"]["id"],
                "album_name": track["album"]["name"],
                "album_release_date": parse_date(track["album"]["release_date"]),
                "artist_id": track["artists"][0]["id"],
                "artist_name": track["artists"][0]["name"]
            }
            new_tracks.append(track_metadata) # append metadata for one song in a playlist
    return new_tracks # return value is a list of dictionaries


def parse_date(date_str):
    if not date_str:
        print("Warning: album_release_date is missing!")
        return None
    try:
        # Try ISO 8601 datetime first
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").date()
    except ValueError:
        pass
    try:
        # Try YYYY-MM-DD format
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        pass
    try:
        # Try year-only and default to January 1st (edge case)
        return datetime.strptime(date_str, "%Y").date()
    except ValueError: # not in any of the formats above
        raise ValueError(f"Unrecognized date format: {date_str}")


def make_json_file():
    """View the data fetched as a json file"""

    tracks_data = get_list_track_details()
    print("\nTotal tracks: ", len(tracks_data))
    with open("test3.json", "w") as out_file:
        json.dump(tracks_data, out_file, indent=4)
        print("\nConverted to json!")
# make_json_file() # uncomment to make json file
