from datetime import date
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType
from pyspark.sql.types import ArrayType, DoubleType, BooleanType

# Get args
hdfs_path = '/user/data/deezer'
today = date.today()
filename = f'deezer-top100-{today}.csv'
csv_path = f'hdfs://namenode:9000{hdfs_path}/{filename}'

# Extract date from filename
raw_date = filename.split('-')[-3:]
d = int(raw_date[2].split('.')[0])
m = int(raw_date[1])
y = int(raw_date[0])
csv_date = date(y, m, d)

# Spark Session
spark = SparkSession \
    .builder \
    .config("spark.sql.warehouse.dir", "hdfs://namenode:9000/user/hive/warehouse") \
    .config("hive.metastore.uris", "thrift://metastore:9083") \
    .config("spark.hadoop.hive.exec.dynamic.partition", "true") \
    .config("spark.hadoop.hive.exec.dynamic.partition.mode", "nonstrict") \
    .appName("Deezer Upload Airflow") \
    .enableHiveSupport() \
    .getOrCreate()

# Define schema
schema = StructType() \
      .add("rank", IntegerType(), True) \
      .add("track_name", StringType(), True) \
      .add("artist_names", StringType(), True) \
      .add("album_name", StringType(), True) \
      .add("source", StringType(), True) \
      .add("uri", StringType(), True) \
      .add("duration", IntegerType(), True) \
      .add("explicit", BooleanType(), True) \

# Read CSV
df = spark.read.format("csv") \
      .option("header", True) \
      .schema(schema) \
      .load(csv_path)

# Add date column nullable value
df = df.withColumn('date', F.when(F.lit(True), F.lit(csv_date)))

# Select columns that will be inserted on the table
df_hive = df.select('rank', 'track_name', 'artist_names', 'source', 'date')

# Write to Hive
df_hive.write \
        .partitionBy("date") \
        .format("hive") \
        .mode("append") \
        .saveAsTable("default.deezer")

spark.stop()