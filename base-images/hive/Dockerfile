FROM base:latest

# Switch to root
USER root

# Set Hive related env vars
ENV HIVE_VERSION 3.1.3
ENV HIVE_URL https://dlcdn.apache.org/hive
ENV HIVE_HOME ${BASE_DIR}/hive
ENV HIVE_CONF_DIR ${HIVE_HOME}/conf
ENV CONF_DIR ${HIVE_CONF_DIR}

# Set Hadoop related env vars
ENV HADOOP_VERSION 3.3.5
ENV HADOOP_URL https://dlcdn.apache.org/hadoop/common
ENV HADOOP_HOME ${BASE_DIR}/hadoop
ENV HADOOP_CONF_DIR ${HADOOP_HOME}/etc/hadoop


# Download Hadoop binary
RUN echo "Downloading Hadoop files..." && \
    curl -fLO "${HADOOP_URL}/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz"  && \
    tar xzvf hadoop-${HADOOP_VERSION}.tar.gz && \
    ln -s hadoop-${HADOOP_VERSION} hadoop && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# Download Hive binary
RUN echo "Downloading Hive files..." && \
    curl -fLO "${HIVE_URL}/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz"  && \
    tar xzvf apache-hive-${HIVE_VERSION}-bin.tar.gz && \
    ln -s apache-hive-${HIVE_VERSION}-bin hive && \
    rm apache-hive-${HIVE_VERSION}-bin.tar.gz

# Set HIVE conf vars
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

# HIVE METASTORE
ENV METASTORE_PORT 9083

# Update PATH
ENV PATH ${PATH}:${HIVE_HOME}/bin/:${HADOOP_HOME}/bin/:${HADOOP_HOME}/sbin/