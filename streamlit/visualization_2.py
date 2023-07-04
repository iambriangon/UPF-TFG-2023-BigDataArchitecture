import streamlit as st
import plotly.express as px
import plotly.graph_objects as pgo
import pandas as pd
from datetime import timedelta
from pyspark.sql import SparkSession
from string_grouper import group_similar_strings

SPOTIFY = 'spotify'
DEEZER = 'deezer'
YOUTUBE = 'youtube'
YOUTUBE_DATE = 'start_date'


@st.cache_data
def get_query(query):
    # Spark Session
    spark = SparkSession \
        .builder \
        .master("spark://spark-master:7077") \
        .config("spark.sql.warehouse.dir", "hdfs://namenode:9000/user/hive/warehouse") \
        .config("hive.metastore.uris", "thrift://metastore:9083") \
        .config("spark.hadoop.hive.exec.dynamic.partition", "true") \
        .config("spark.hadoop.hive.exec.dynamic.partition.mode", "nonstrict") \
        .appName("Streamlit query") \
        .enableHiveSupport() \
        .getOrCreate()

    # Get resulting query
    df_result = spark.sql(query).toPandas()

    return df_result


def get_dates(table: str, date_col='date'):
    q = f"""
    SELECT distinct(`{date_col}`) 
    FROM {table}    
    ORDER BY `{date_col}` DESC
    """
    df = get_query(q)
    return df


def get_top(table: str, date: str, date_col='date'):
    q = f'''
    SELECT * 
    FROM {table}
    WHERE `{date_col}` = "{date}"
    ORDER BY rank ASC
    '''

    df = get_query(q)
    return df


def get_number_of_artist_occurrences(table: str, date: str, date_col='date'):
    q = f'''
    SELECT count(*) as artist_count, artist
    FROM 
    (
    SELECT explode(split(artist_names, ", ")) AS artist
    FROM {table}
    WHERE `{date_col}` = "{date}"
    ) AS aux
    GROUP BY artist
    ORDER BY artist_count DESC
    '''

    df = get_query(q)

    return df


def get_number_of_label_occurrences(table: str, date: str, date_col='date'):
    q = f'''
    SELECT source, track_name
    FROM {table}
    WHERE `{date_col}` = "{date}"
    '''

    df_labels = get_query(q)

    # Cols:[group_rep_index, group_rep_source]
    df_labels[['group_rep_index', 'group_rep_source']] = group_similar_strings(df_labels['source'], min_similarity=0.80)
    df_grouped_labels = df_labels['group_rep_source'].value_counts().to_frame().reset_index()

    return df_labels, df_grouped_labels


def get_number_of_artist_per_song(table: str, date: str, date_col='date'):
    q = f'''
    SELECT size(split(artist_names, ", ")) AS number_of_artists, split(artist_names, ", ") AS artists, track_name
    FROM {table}
    WHERE `{date_col}` = "{date}"
    '''

    df = get_query(q)
    df_grouped = df['number_of_artists'].value_counts().to_frame().reset_index()

    return df, df_grouped


def get_track_evolution(table: str, track: str):
    q = f'''
        SELECT rank, `date`
        FROM {table}
        WHERE track_name = "{track}"
        ORDER BY `date` ASC
        '''
    df = get_query(q)

    return df


def get_weekly(table: str, date):
    start = date
    end = start + timedelta(days=6)

    q = f'''
        SELECT track_name, ROUND(AVG(rank)) AS rank 
        FROM {table} 
        WHERE `date` BETWEEN "{start}" AND "{end}"
        GROUP BY track_name
        ORDER BY rank ASC 
        '''

    df = get_query(q)

    return df


def main_page():
    st.header('Music Charts')
    st.subheader('Final Thesis Project - 2023 UPF')



def spotify_page():
    st.header('Spotify Charts Spain')

    df_date = get_dates(table=SPOTIFY)
    date = st.selectbox('Select date', df_date)

    st.markdown(f'### Data statistics of {date}')

    ##########
    st.markdown('#### Top 200 Spotify Spain')
    df_top = get_top(table=SPOTIFY, date=date)
    st.write(df_top)

    ###########
    st.markdown(f'#### Number of songs in chart per artists on {date}')
    df_artist_occurrences = get_number_of_artist_occurrences(table=SPOTIFY, date=date)

    left, right = st.columns(2)
    with left:
        st.write(df_artist_occurrences)

    with right:
        st.plotly_chart(px.pie(df_artist_occurrences.head(20), values='artist_count', names='artist',
                               title='Number of songs per artist (TOP 20)'))

    #########
    st.markdown(f'#### Number of songs in chart per record label on {date}')
    df_original_labels, df_grouped_labels = get_number_of_label_occurrences(table=SPOTIFY, date=date)
    left, right = st.columns(2)
    with left:
        st.write(df_original_labels)

    with right:
        st.plotly_chart(px.pie(df_grouped_labels, values='count', names='group_rep_source',
                               title='Number of songs per record label'))

    #########
    st.markdown(f'#### Number of artists per song on {date}')
    df_artists_per_song, df_artists_per_song_count = get_number_of_artist_per_song(table=SPOTIFY, date=date)

    left, right = st.columns(2)
    with left:
        st.write(df_artists_per_song)

    with right:
        st.plotly_chart(px.pie(df_artists_per_song_count, values='count', names='number_of_artists',
                               title='Number of artists per song'))

    #########
    track = st.selectbox("Track:", df_top['track_name'])
    st.subheader(f"Daily evolution of {track}")
    df_track_evolution = get_track_evolution(table=SPOTIFY, track=track)

    left, right = st.columns(2)
    with left:
        st.write(df_track_evolution)

    with right:
        st.plotly_chart(px.line(df_track_evolution, x='date', y='rank', title=f'Daily evolution of {track}'))


def deezer_page():
    st.header('Deezer Charts Spain')

    df_date = get_dates(table=DEEZER)
    date = st.selectbox('Select date', df_date)

    st.markdown(f'### Data statistics of {date}')

    ##########
    st.markdown('#### Top 100 Deezer Spain')
    df_top = get_top(table=DEEZER, date=date)
    st.write(df_top)

    ###########
    st.markdown(f'#### Number of songs in chart per artists on {date}')
    df_artist_occurrences = get_number_of_artist_occurrences(table=DEEZER, date=date)

    left, right = st.columns(2)
    with left:
        st.write(df_artist_occurrences)

    with right:
        st.plotly_chart(px.pie(df_artist_occurrences.head(20), values='artist_count', names='artist',
                               title='Number of songs per artist (TOP 20)'))

    #########
    st.markdown(f'#### Number of songs in chart per record label on {date}')
    df_original_labels, df_grouped_labels = get_number_of_label_occurrences(table=DEEZER, date=date)
    left, right = st.columns(2)
    with left:
        st.write(df_original_labels)

    with right:
        st.plotly_chart(px.pie(df_grouped_labels, values='count', names='group_rep_source',
                               title='Number of songs per record label'))

    #########
    st.markdown(f'#### Number of artists per song on {date}')
    df_artists_per_song, df_artists_per_song_count = get_number_of_artist_per_song(table=DEEZER, date=date)

    left, right = st.columns(2)
    with left:
        st.write(df_artists_per_song)

    with right:
        st.plotly_chart(px.pie(df_artists_per_song_count, values='count', names='number_of_artists',
                               title='Number of artists per song'))


def youtube_page():
    st.header('Youtube Charts Spain')

    df_date = get_dates(table=YOUTUBE, date_col=YOUTUBE_DATE)
    date = st.selectbox('Select date', df_date)

    st.markdown(f'### Data statistics of {date}')

    #########
    st.markdown('#### Top 200 Youtube Spain')
    df_top = get_top(table=YOUTUBE, date=date, date_col=YOUTUBE_DATE)
    st.write(df_top)


def all_sources_page():
    st.header('Youtube/Deezer/Spotify Data')

    df_date = get_dates(table=YOUTUBE, date_col=YOUTUBE_DATE)
    date = st.selectbox('Select date', df_date)

    df_spotify_weekly = get_weekly(table=SPOTIFY, date=date).head(10)
    df_youtube_weekly = get_top(table=YOUTUBE, date=date, date_col=YOUTUBE_DATE).head(10)
    df_youtube_spotify_weekly = pd.merge(df_spotify_weekly, df_youtube_weekly, on='track_name', how='outer').fillna(0)
    df_youtube_spotify_weekly[['group_rep_index', 'group_rep_source']] = group_similar_strings(
        df_youtube_spotify_weekly['track_name'], min_similarity=0.30)

    st.markdown(f'#### Ranking comparison (TOP 10) Spotify - Youtube for the week {date}')

    left, right = st.columns(2)

    with left:
        st.markdown('#### SPOTIFY')
        st.write(df_spotify_weekly)

    with right:
        st.markdown('#### YOUTUBE')
        st.write(df_youtube_weekly[['track_name', 'rank']])

    both_fig = pgo.Figure(data=[pgo.Bar(
        name='Spotify Rank',
        x=df_youtube_spotify_weekly.group_rep_source,
        y=df_youtube_spotify_weekly.rank_x
    ),
        pgo.Bar(
            name='Youtube Rank',
            x=df_youtube_spotify_weekly.group_rep_source,
            y=df_youtube_spotify_weekly.rank_y
        )
    ])

    st.plotly_chart(both_fig)


def interactive_page():
    st.header('Run your queries interactively')

    text_input = st.text_input(
        label='Try your queries here!',
        placeholder='Write your SQL query'
    )

    if text_input:
        st.write(get_query(text_input))

    else:
        st.write("Your query is empty!")


if __name__ == "__main__":
    st.set_page_config(page_title='Music Chart Analysis', layout='wide')
    page = st.sidebar.selectbox('Select page',
                                ['Home', 'Spotify', 'Youtube', 'Deezer', 'Interactive', 'All data sources'])

    if page == 'Home':
        main_page()

    elif page == 'Spotify':
        spotify_page()

    elif page == 'Youtube':
        youtube_page()

    elif page == 'Deezer':
        deezer_page()

    elif page == 'Interactive':
        interactive_page()

    else:
        all_sources_page()
