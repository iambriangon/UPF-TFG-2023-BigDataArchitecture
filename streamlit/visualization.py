import streamlit as st
import plotly.express as px
from pyspark.sql import SparkSession
from string_grouper import group_similar_strings


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


def main_page():
    st.header('Music Charts')
    st.subheader('Final Thesis Project - 2023 UPF')


def spotify_page():
    st.header('Spotify Charts Spain')

    df_date = get_query("""
    SELECT distinct(`date`) 
    FROM spotify
    ORDER BY `date` DESC
    """)
    date = st.selectbox('Select date', df_date)

    st.markdown(f'### Data statistics of {date}')

    st.markdown('#### Top 200 Spotify Spain')
    df = get_query(f'''
    SELECT * 
    FROM spotify
    WHERE `date` = "{date}"
    ORDER BY rank ASC
    ''')
    st.write(df)

    st.markdown(f'#### Number of songs per artists in {date} chart (TOP 20)')
    df = get_query(f'''
    SELECT count(*) as artist_count, artist
    FROM 
    (
    SELECT explode(split(artist_names, ", ")) AS artist
    FROM spotify
    WHERE `date` = "{date}"
    ) AS aux
    GROUP BY artist
    ORDER BY artist_count DESC
    LIMIT 20
    '''
    )
    fig = px.pie(df, values='artist_count', names='artist', title='Number of songs per artist in chart')
    st.plotly_chart(fig)

    """
    st.markdown(f'#### Record label representation')
    df[['group_rep_id', 'group_rep']] = group_similar_strings(
        df['source'],
        min_similarity=0.8
    )
    st.write(df)
    """


def deezer_page():
    st.header('Deezer Charts Spain')

    left, right = st.columns(2)
    with left:
        st.write("I am left col")

    with right:
        st.write("I am right col")


def youtube_page():
    st.header('Youtube Charts Spain')


def all_sources_page():
    st.header('Youtube/Deezer/Spotify Data')


if __name__ == "__main__":
    st.set_page_config(page_title='Music Chart Analysis', layout='wide')
    page = st.sidebar.selectbox('Select page', ['Home', 'Spotify', 'Youtube', 'Deezer', 'All data sources'])

    if page == 'Home':
        main_page()

    elif page == 'Spotify':
        spotify_page()

    elif page == 'Youtube':
        youtube_page()

    elif page == 'Deezer':
        deezer_page()

    else:
        all_sources_page()
