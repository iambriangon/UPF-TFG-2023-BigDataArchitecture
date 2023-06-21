from pywebhdfs.webhdfs import PyWebHdfsClient
import requests
import json
import re


def upload_to_hdfs(host='namenode', port='9870', user_name='root', hdfs_path=None, file=None):
    hdfs = PyWebHdfsClient(host=host, port=port, user_name=user_name)

    if hdfs_path is None or file is None:
        raise Exception("No HDFS path or file provided!")
    else:
        # Hacer try catch si file existe
        return hdfs.create_file(hdfs_path, file)


def get_youtube_chart():
    YOUTUBE_CHARTS_URL = 'https://charts.youtube.com/charts/TopSongs/es'
    r = requests.get(YOUTUBE_CHARTS_URL)

    html = r.text
    apiKey = re.search('"INNERTUBE_API_KEY":"(.+?)"', html).group(1)

    YOUTUBE_CHARTS_API = f'https://charts.youtube.com/youtubei/v1/browse?alt=json&key={apiKey}'
    r = requests.post(YOUTUBE_CHARTS_API,
                      json={
                          'context': {
                              'client': {
                                  'clientName': "WEB_MUSIC_ANALYTICS",
                                  'clientVersion': "0.2",
                                  'hl': "ES",
                                  'gl': "es",
                                  'experimentIds': [],
                                  'experimentsToken': "",
                                  'theme': "MUSIC",
                              },
                              'capabilities': {},
                              'request': {
                                  'internalExperimentFlags': [],
                              },
                          },
                          'browseId': "FEmusic_analytics_charts_home",
                          'query': "chart_params_type=WEEK&perspective=CHART&flags=viral_video_chart&selected_chart=TRACKS&chart_params_id=weekly%3A0%3A0%3Aes",
                      },
                      headers={
                          'referer': 'https://charts.youtube.com/charts/TopSongs/es'
                      })

    response = json.loads(r.text)
    return response['contents']['sectionListRenderer']['contents'][0]['musicAnalyticsSectionRenderer']['content'][
        'trackTypes'][0]
