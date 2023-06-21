import sys
from datetime import date, timedelta
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType
from pyspark.sql.types import ArrayType, DoubleType, BooleanType

# Set vars
hdfs_path = '/user/data/youtube'
today = date.today()
chart_date = today + timedelta(days=(3 - today.weekday()) % 7) - timedelta(days=7)
filename = f'youtube-top100-{chart_date}.csv'
csv_path = f'hdfs://namenode:9000{hdfs_path}/{filename}'

# Extract date from filename
raw_date = filename.split('-')[-3:]
d = int(raw_date[2].split('.')[0])
m = int(raw_date[1])
y = int(raw_date[0])

end_date = date(y, m, d)
start_date = end_date - timedelta(days=6)

# Spark Session
spark = SparkSession \
    .builder \
    .config("spark.sql.warehouse.dir", "hdfs://namenode:9000/user/hive/warehouse") \
    .config("hive.metastore.uris", "thrift://metastore:9083") \
    .config("spark.hadoop.hive.exec.dynamic.partition", "true") \
    .config("spark.hadoop.hive.exec.dynamic.partition.mode", "nonstrict") \
    .appName("Youtube Upload Airflow") \
    .enableHiveSupport() \
    .getOrCreate()


# Define schema
schema = StructType() \
      .add("rank", IntegerType(), True) \
      .add("previous_rank", IntegerType(), True) \
      .add("track_name", StringType(), True) \
      .add("artist_names", StringType(), True) \
      .add("weeks_on_chart", IntegerType(), True) \
      .add("views", IntegerType(), True) \
      .add("weekly_growth", StringType(), True) \
      .add("youtube_url", StringType(), True) \


# Read CSV
df = spark.read.format("csv") \
      .option("header", True) \
      .schema(schema) \
      .load(csv_path)

# Add date column nullable value
df = df.withColumn('start_date', F.when(F.lit(True), F.lit(start_date)))\
    .withColumn('end_date', F.when(F.lit(True), F.lit(end_date)))

# Select columns that will be inserted on the table
df_hive = df.select('rank', 'artist_names', 'track_name', 'start_date', 'end_date')


# Write to Hive
df_hive.write \
        .partitionBy("end_date") \
        .format("hive") \
        .mode("append") \
        .saveAsTable("default.youtube")

spark.stop()
