#!/bin/bash

DIR=$(pwd)
echo $DIR

cd $DIR/base-images/base
docker build -t base .

cd $DIR/base-images/hadoop
docker build -t hadoop .

cd $DIR/base-images/hive
docker build -t hive .

cd $DIR/base-images/spark
docker build -t spark .
