from etl.spotify_load import setup_database, insert_metadata
from etl.spotify_extract_transform import get_list_track_details

def main():
    session, engine = setup_database()

    tracks = get_list_track_details()

    num_tracks_inserted = 0
    for track in tracks:
        num_tracks_inserted += insert_metadata(session, track)

    session.close()

    print(f"\n{num_tracks_inserted} tracks inserted into database since the last refresh!\n")
    
    num_of_tracks = len(tracks)
    print(f"All {num_of_tracks} tracks have potentially been inserted!")

if __name__ == "__main__":
    main()




