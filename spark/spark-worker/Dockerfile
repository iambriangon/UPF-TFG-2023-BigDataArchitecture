FROM spark:latest

# Set env specifics for worker
ENV SPARK_WORKER_MEMORY=1G
ENV SPARK_WORKER_CORES=1

# Init worker
CMD ${SPARK_HOME}/sbin/start-worker.sh spark://spark-master:7077
