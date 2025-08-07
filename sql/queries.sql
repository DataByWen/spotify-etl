-- How many tracks appear in more than one playlist?
SELECT track_id, count(playlist_id) as count
FROM playlist_tracks
GROUP BY track_id
HAVING count > 1; 

 -- Get the 10 newest tracks added
SELECT t.track_id, pt.playlist_id,t.track_name, pt.track_added_at
FROM tracks as t
JOIN playlist_tracks as pt
ON t.track_id = pt.track_id
ORDER BY pt.track_added_at DESC
LIMIT 10;

-- Find tracks that were added on a certain date
SELECT t.track_name, t.track_id, pt.track_added_at
FROM tracks t 
JOIN playlist_tracks pt
ON t.track_id = pt.track_id
WHERE pt.track_added_at = "2025-06-24";

-- Find tracks that appear in more than one playlist
SELECT 
    playlist_tracks.track_id, 
    COUNT(playlist_tracks.playlist_id) AS count, 
    tracks.track_name,
    artists.artist_name
FROM playlist_tracks
JOIN tracks ON playlist_tracks.track_id = tracks.track_id
JOIN artists ON tracks.artist_id = artists.artist_id
GROUP BY playlist_tracks.track_id, tracks.track_name, artists.artist_name
HAVING count > 1
ORDER BY count DESC;

-- Are there songs that appear in all 3 playlists? 
SELECT 
    playlist_tracks.track_id, 
    COUNT(playlist_tracks.playlist_id) AS count, 
    tracks.track_name,
    artists.artist_name
FROM playlist_tracks
JOIN tracks ON playlist_tracks.track_id = tracks.track_id
JOIN artists ON tracks.artist_id = artists.artist_id
GROUP BY playlist_tracks.track_id, tracks.track_name, artists.artist_name
HAVING count = 3;

-- What artists have the most songs across these 3 playlists?
SELECT 
	artists.artist_name,
    COUNT(playlist_tracks.track_id) AS num_songs
FROM playlist_tracks
JOIN tracks ON playlist_tracks.track_id = tracks.track_id
JOIN artists ON tracks.artist_id = artists.artist_id    
WHERE playlist_tracks.playlist_id IN (
    '6dAlzHQLVuZQZdMrzEETjB',
    '5Wy63I49cRoBAE2dWUApH5',
    '3asriXKNT1yYcOPD7HNTY8'
)
GROUP BY artists.artist_id, artists.artist_name
ORDER BY num_songs DESC;
    
    
-- Identify tracks shared between two specific playlists (1)
SELECT COUNT(*) AS num_common_tracks
FROM (
    SELECT track_id
    FROM playlist_tracks
    WHERE playlist_id IN ('6dAlzHQLVuZQZdMrzEETjB', '5Wy63I49cRoBAE2dWUApH5')
    GROUP BY track_id
    HAVING COUNT(DISTINCT playlist_id) = 2
) AS common_tracks;

-- Identify tracks shared between two specific playlists (2)
SELECT COUNT(*) AS num_common_tracks
FROM (
    SELECT track_id
    FROM playlist_tracks
    WHERE playlist_id IN ('5Wy63I49cRoBAE2dWUApH5', '3asriXKNT1yYcOPD7HNTY8')
    GROUP BY track_id
    HAVING COUNT(DISTINCT playlist_id) = 2
) AS common_tracks;

-- Identify tracks shared between two specific playlists (3)
SELECT COUNT(*) AS num_common_tracks
FROM (
    SELECT track_id
    FROM playlist_tracks
    WHERE playlist_id IN ('6dAlzHQLVuZQZdMrzEETjB', '3asriXKNT1yYcOPD7HNTY8')
    GROUP BY track_id
    HAVING COUNT(DISTINCT playlist_id) = 2
) AS common_tracks;


-- Identify tracks shared between all 3 playlists
SELECT COUNT(*) AS num_common_tracks
FROM (
    SELECT track_id
    FROM playlist_tracks
    WHERE playlist_id IN ('6dAlzHQLVuZQZdMrzEETjB', '3asriXKNT1yYcOPD7HNTY8', '5Wy63I49cRoBAE2dWUApH5')
    GROUP BY track_id
    HAVING COUNT(DISTINCT playlist_id) = 3
) AS common_tracks; -- 1
