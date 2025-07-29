# Spotify Playlist DB

An end-to-end pipeline that pulls track data from Spotify playlists via the Spotify API, loads it into a relational database, and supports in-depth data analysis.


## How This Works

```mermaid
flowchart TD
    A[Start ETL Process] --> B[Extract: Fetch data from Spotify API]
    B --> C[Transform: Clean and structure data with Pandas]
    C --> D[Load: Connect to MySQL. Insert data into tables using SQLAlchemy]
    D --> E[End ETL Process]

    subgraph Spotify API
        B
    end

    subgraph MySQL Database
        D
    end
```


## Database Schema
The database is normalized to 3NF.

```mermaid
erDiagram

    Playlist ||--o{ Playlist_Tracks : contains
    Track ||--o{ Playlist_Tracks : appears_in
    Track }o--|| Album : consists_of
    Track }o--|| Artist : creates

    Playlist {
        varchar playlist_id PK
        varchar playlist_user_id
    }

    Playlist_Tracks {
        varchar track_id PK, FK
        varchar playlist_id PK, FK
        date track_added_at
    }

    Track {
        varchar track_id PK
        varchar track_name
        float track_duration_mins
        varchar track_uri
        int popularity
        bool explicit_track
        varchar album_id FK
        varchar artist_id FK
    }

    Album {
        varchar album_id PK
        varchar album_name
        date album_release_date
    }

    Artist {
        varchar artist_id PK
        varchar artist_name
    }
```
