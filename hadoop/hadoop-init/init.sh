#!/bin/bash

echo  "Creating necessary directories..."

hdfs dfs -mkdir -p hdfs://namenode:9000/tmp
hdfs dfs -chmod g+w hdfs://namenode:9000/tmp 

hdfs dfs -mkdir -p hdfs://namenode:9000/user/hive/warehouse
hdfs dfs -chmod g+w hdfs://namenode:9000/user/hive/warehouse

hdfs dfs -mkdir -p hdfs://namenode:9000/tmp/hive
hdfs dfs -chmod 777 hdfs://namenode:9000/tmp/hive

hdfs dfs -mkdir -p hdfs://namenode:9000/user/data/spotify
hdfs dfs -chmod 777 hdfs://namenode:9000/user/data/spotify

hdfs dfs -mkdir -p hdfs://namenode:9000/user/data/youtube
hdfs dfs -chmod 777 hdfs://namenode:9000/user/data/youtube

hdfs dfs -mkdir -p hdfs://namenode:9000/user/data/deezer
hdfs dfs -chmod 777 hdfs://namenode:9000/user/data/deezer

echo "Done!"