import pandas as pd
from datetime import datetime, date, timedelta
from utils import upload_to_hdfs, get_youtube_chart


data = get_youtube_chart()

"""
date_format = '%Y-%m-%d'
playlist_end_date = data['endDate']
chart_end_date = datetime.strptime(playlist_end_date, date_format).date()
"""

chartDf = pd.DataFrame(
    columns=['rank', 'previous_rank', 'track_name', 'artist_names', 'weeks_on_chart', 'views', 'weekly_growth',
             'youtube_url'])

tracks = data['trackViews']

for i, track in enumerate(tracks):
    rank = track['chartEntryMetadata']['currentPosition']
    track_name = track['name']
    artists_names = list(map(lambda x: x['name'], track['artists']))
    views = track['viewCount']
    youtube_url = f'https://www.youtube.com/watch?v={track["encryptedVideoId"]}'
    weeks_on_chart = track['chartEntryMetadata']['periodsOnChart']

    if len(artists_names) < 3:
        artists_names = ' & '.join(artists_names)
    else:
        artists_names = ', '.join(artists_names[:-1]) + ' & ' + artists_names[-1]

    if 'previousPosition' in track['chartEntryMetadata']:
        previous_rank = track['chartEntryMetadata']['previousPosition']
    else:
        previous_rank = -1

    if 'percentViewsChange' in track['chartEntryMetadata']:
        weekly_growth = f'{round(track["chartEntryMetadata"]["percentViewsChange"] * 100, 1)}%'
    else:
        weekly_growth = '0%'

    track_info = {
        'rank': rank,
        'previous_rank': previous_rank,
        'track_name': track_name,
        'artist_names': artists_names,
        'weeks_on_chart': weeks_on_chart,
        'views': views,
        'weekly_growth': weekly_growth,
        'youtube_url': youtube_url
    }
    chartDf.loc[i] = track_info


today = date.today()
chart_date = today + timedelta(days=(3 - today.weekday()) % 7) - timedelta(days=7)

path = f'user/data/youtube/youtube-top100-{chart_date}.csv'

# Write CSV to HDFS
upload_to_hdfs(hdfs_path=path, file=chartDf.to_csv(index=False).encode('utf-8'))

