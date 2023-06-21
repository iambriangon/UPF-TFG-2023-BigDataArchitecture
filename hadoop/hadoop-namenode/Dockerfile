FROM hadoop:latest

# namenode dir
RUN mkdir -p ${HDFS_DATA_DIR}/namenode

# Format namenode if is not formatted
# Init namenode
CMD hdfs namenode -format -nonInteractive && hdfs namenode
