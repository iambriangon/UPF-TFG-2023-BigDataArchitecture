import spotipy
import pandas as pd
import time
from credentials import spotify_access_tokens
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import date
from utils import upload_to_hdfs

# HDFS Path for Deezer data
today = date.today()
path = f'user/data/spotify/spotify-top50-{today}.csv'

# Dataframe Schema
chartDf = pd.DataFrame(columns=['rank', 'uri', 'artist_names', 'track_name', 'source'])

# Auth for Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_access_tokens['CLIENT_ID'],
                                                           client_secret=spotify_access_tokens['CLIENT_SECRET']))

# Query TOP50 Spain
playlist = sp.playlist_items(playlist_id='37i9dQZEVXbNFJfN1Vw8d9', fields='items')

"""
# Get date of playlist
playlist_date = playlist['items'][0]['added_at']
date_format = '%Y-%m-%dT%H:%M:%SZ'
chartDate = datetime.strptime(playlist_date, date_format).date()
"""

# Create Dataframe
for rank, item in enumerate(playlist['items']):
    chartRank = rank + 1
    songName = item['track']['name']
    uri = item['track']['uri']
    source = sp.album(item['track']['album']['id'])['label']
    artists = []
    for artist in item['track']['artists']:
        artists.append(artist['name'])

    songDict = {
        'rank': chartRank,
        'uri': uri,
        'artist_names': ', '.join(artists),
        'track_name': songName,
        'source': source
    }
    chartDf.loc[rank] = songDict

    # Wait between calls to the API
    time.sleep(100/1000)

# Write CSV to HDFS
upload_to_hdfs(hdfs_path=path, file=chartDf.to_csv(index=False).encode('utf-8'))


