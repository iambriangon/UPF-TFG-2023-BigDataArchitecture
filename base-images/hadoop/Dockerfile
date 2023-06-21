FROM base:latest

# Switch to root
USER root

# Set Hadoop related env vars
ENV HADOOP_VERSION 3.3.5
ENV HADOOP_URL https://dlcdn.apache.org/hadoop/common
ENV HADOOP_HOME ${BASE_DIR}/hadoop
ENV HADOOP_CONF_DIR ${HADOOP_HOME}/etc/hadoop
ENV HDFS_DATA_DIR /var/data/hadoop/hdfs
ENV CONF_DIR ${HADOOP_CONF_DIR}

# Download Hadoop binary
RUN echo "Downloading Hadoop files..." && \
    curl -fLO "${HADOOP_URL}/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz"  && \
    tar xzvf hadoop-${HADOOP_VERSION}.tar.gz && \
    ln -s hadoop-${HADOOP_VERSION} hadoop && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# Set Hadoop conf vars
ENV CORE_SITE_CONF_fs_defaultFS hdfs://namenode:9000
ENV HDFS_SITE_CONF_dfs_replication 1
ENV HDFS_SITE_CONF_dfs_namenode_name_dir file:///var/data/hadoop/hdfs/namenode
ENV HDFS_SITE_CONF_dfs_datanode_data_dir file:///var/data/hadoop/hdfs/datanode
ENV HDFS_SITE_CONF_dfs_namenode_http-address namenode:9870
ENV HDFS_SITE_CONF_dfs_webhdfs_enabled true

# Make dir for logs
RUN mkdir ${HADOOP_HOME}/logs

# Update PATH
ENV PATH ${PATH}:${HADOOP_HOME}/bin/:${HADOOP_HOME}/sbin/