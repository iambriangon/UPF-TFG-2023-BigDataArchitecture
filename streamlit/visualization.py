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

    st.subheader('Run your queries interactively')

    text_input = st.text_input(
        label='Try your queries here!',
        placeholder='Write your SQL query'
    )

    if text_input:
        st.write(get_query(text_input))

    else:
        st.write("Your query is empty!")


def about_page():
    st.header('About')
    st.subheader('This application has been made by Brayan Gonzalez, UPF-Barcelona Student as part of his final degree project')


if __name__ == "__main__":
    st.set_page_config(page_title='Music Chart Analysis', layout='wide')
    page = st.sidebar.selectbox('Select page', ['Home', 'About'])

    if page == 'Home':
        main_page()

    else:
        about_page()
