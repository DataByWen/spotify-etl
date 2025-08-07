from sqlalchemy import  Column, Integer, String, Float, Date, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from etl.spotify_extract_transform import get_list_track_details

Base = declarative_base() # set up a Base class that all tables will inherit from

def setup_database():
    """Connect to database server"""
    DATABASE_URL = "mysql+mysqlconnector://root@localhost/spotify_database"
    engine = create_engine(DATABASE_URL, echo=True) # echo=True logs all the SQL statements to the terminal
    Base.metadata.create_all(engine) # creates the database tables
    Session = sessionmaker(bind=engine) # sessionmaker is a factory that creates new Session objects
    session = Session() 
    return session, engine


# tables are normalized to third normal form
class Track(Base):
    __tablename__ = 'tracks' # creates table if it doesn't exist
    
    track_id = Column(String(255), primary_key=True, unique=True, nullable=False)
    track_name = Column(String(255), nullable=False) 
    track_duration_mins = Column(Float)
    track_uri = Column(String(255))
    popularity = Column(Integer)
    explicit_track = Column(Boolean)
    album_id = Column(String(255), ForeignKey("albums.album_id"))
    artist_id = Column(String(255), ForeignKey("artists.artist_id"))

    # Relationships: these are also attributes of the class
    # back_populates: a bidirectional relationship (you can access attributes both ways)
    album = relationship("Album", back_populates="tracks")
    artist = relationship("Artist", back_populates="tracks")
    playlist_tracks = relationship("Playlist_Track", back_populates="track")


class Album(Base): 
    __tablename__ = 'albums'   

    album_id = Column(String(255), primary_key=True)
    album_name = Column(String(255))
    album_release_date = Column(Date) 

    tracks = relationship("Track", back_populates="album")


class Artist(Base):
    __tablename__ = 'artists'  
    
    artist_id = Column(String(255), primary_key=True)
    artist_name = Column(String(255))

    tracks = relationship("Track", back_populates="artist")


class Playlist(Base):
    __tablename__ = 'playlists'

    playlist_id = Column(String(255), primary_key=True)
    playlist_user_id = Column(String(255))

    playlist_tracks = relationship("Playlist_Track", back_populates="playlist")
    
    
class Playlist_Track(Base): 
    __tablename__ = 'playlist_tracks'  

    track_id = Column(String(255), ForeignKey("tracks.track_id"), primary_key=True)
    playlist_id = Column(String(255), ForeignKey("playlists.playlist_id"), primary_key=True)
    track_added_at = Column(Date) 

    track = relationship("Track", back_populates="playlist_tracks")
    playlist = relationship("Playlist", back_populates="playlist_tracks")


def insert_metadata(session, track) -> int:
    """Insert metadata for 1 track into the database. Returns 1 if track was successfully inserted. Otherwise, 0 is returned."""
    pt = session.get(Playlist_Track, (track["track_id"], track["playlist_id"]))

    # Ensure rerunning the script does not insert duplicate records into the database
    if pt: 
        print("The track and playlist info has been added already so pass")
        return 0
    
    else: # insert only if the combo DNE
        try:
            print("Not found so this pt combo will be added")
            
            # 1. insert album
            album = session.get(Album, track["album_id"])
            if not album:
                album = Album(
                    album_id = track["album_id"],
                    album_name = track["album_name"],
                    album_release_date = track["album_release_date"]  # make sure this is a datetime.date object
                )
                session.add(album)

            # 2. insert artist
            artist = session.get(Artist, track["artist_id"])
            if not artist:
                artist = Artist(
                    artist_id = track["artist_id"],
                    artist_name = track["artist_name"]
                )
                session.add(artist)

            # 3. insert track
            song = session.get(Track, (track["track_id"]))
            if not song:
                song = Track(
                    track_id = track["track_id"],
                    track_name = track["track_name"],
                    track_duration_mins = track["track_duration_mins"],
                    track_uri = track["track_uri"],
                    popularity = track["popularity"],
                    explicit_track = track["explicit_track"],
                    album_id = track["album_id"],
                    artist_id = track["artist_id"]
                )
                session.add(song) # add the row

            # 4. insert playlist
            playlist = session.get(Playlist, track["playlist_id"])
            if not playlist:
                playlist = Playlist(
                    playlist_id = track["playlist_id"],
                    playlist_user_id = track["playlist_user_id"]
                )
                session.add(playlist)

            # 5. insert playlist_track
            playlist_track = Playlist_Track(
                track_id = track["track_id"],
                playlist_id = track["playlist_id"],
                track_added_at = track["track_added_at"]
            )
            session.add(playlist_track) # add the row 
            session.commit()
            return 1
        
        except Exception as e: # track doesn't exist in database but there is some error with the track (e.g. song is not available anymore so we don't insert into the db)
            session.rollback()  # Undo any partial changes
            print("Something went wrong:", e)
            print(f"Failed to insert data for track: {track['track_name']}. The user id of the playlist is {track['playlist_user_id']}")
            return 0 
