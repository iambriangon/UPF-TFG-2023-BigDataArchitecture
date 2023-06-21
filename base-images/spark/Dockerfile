FROM base:latest

# Switch to root
USER root

# Set Spark related env vars
ENV SPARK_VERSION 3.4.0
ENV SPARK_URL https://dlcdn.apache.org/spark
ENV SPARK_HOME ${BASE_DIR}/spark
ENV SPARK_CONF_DIR ${SPARK_HOME}/conf
ENV CONF_DIR ${SPARK_CONF_DIR}


# Download Spark binary
RUN echo "Downloading Spark files..." && \
    curl -fLO "${SPARK_URL}/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz"  && \
    tar xzvf spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    ln -s spark-${SPARK_VERSION}-bin-hadoop3 spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

# Set Conf files
# HADOOP
ENV CORE_SITE_CONF_fs_defaultFS hdfs://namenode:9000
ENV HDFS_SITE_CONF_dfs_replication 1
ENV HDFS_SITE_CONF_dfs_namenode_name_dir file:///var/data/hadoop/hdfs/namenode
ENV HDFS_SITE_CONF_dfs_datanode_data_dir file:///var/data/hadoop/hdfs/datanode
ENV HDFS_SITE_CONF_dfs_namenode_http-address namenode:9870
ENV HDFS_SITE_CONF_dfs_webhdfs_enabled true

# HIVE GENERAL
ENV HIVE_SITE_CONF_hive_querylog_location /usr/local/hive/log/hive.log
ENV HIVE_SITE_CONF_hive_querylog_enable_plan_progress false
ENV HIVE_SITE_CONF_hive_log_explain_output false
ENV HIVE_SITE_CONF_hive_resultset_use_unique_column_names false

# HIVE SERVER
ENV HIVE_SITE_CONF_hive_server2_enable_doAs false
ENV HIVE_SITE_CONF_hive_metastore_event_db_notification_api_auth false

# HIVE SPARK
ENV HIVE_SITE_CONF_hive_metastore_schema_verification false
ENV HIVE_SITE_CONF_hive_metastore_warehouse_dir hdfs://namenode:9000/user/hive/warehouse
ENV HIVE_SITE_CONF_hive_metastore_uris thrift://metastore:9083

# Set Spark variables
ENV SPARK_MASTER_PORT 7077
ENV SPARK_USER spark
ENV SPARK_NO_DAEMONIZE true

# Update PATH
ENV PATH ${PATH}:${SPARK_HOME}/bin/:${SPARK_HOME}/sbin/

