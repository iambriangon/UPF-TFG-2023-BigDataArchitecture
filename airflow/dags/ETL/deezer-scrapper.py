import deezer
import time
import pandas as pd
from datetime import date
from utils import upload_to_hdfs

# HDFS Path for Spotify data
today = date.today()
path = f'user/data/deezer/deezer-top100-{today}.csv'


# Dataframe Schema
chartDf = pd.DataFrame(columns=['rank', 'track_name', 'artist_names', 'album_name', 'source', 'uri', 'duration', 'explicit'])

# Deezer Client
client = deezer.Client()
top_100_spain_id = 1116190041

# Query TOP100 Spain
tracks = client.get_playlist(playlist_id=top_100_spain_id).tracks


# Create Dataframe
for rank, track in enumerate(tracks):
    artists = ', '.join(list(map(lambda artist: artist.name, track.contributors)))
    track_info = {
        'rank': rank + 1,
        'track_name': track.title,
        'artist_names': artists,
        'album_name': track.album.title,
        'source': track.album.label,
        'uri': track.link,
        'duration': track.duration,
        'explicit': track.explicit_lyrics
    }
    chartDf.loc[rank] = track_info

    # To not overload Deezer API, wait between calls
    time.sleep(200/1000)

# Write CSV to HDFS
upload_to_hdfs(hdfs_path=path, file=chartDf.to_csv(index=False).encode('utf-8'))











