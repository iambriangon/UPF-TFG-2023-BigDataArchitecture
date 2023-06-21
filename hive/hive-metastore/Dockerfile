FROM hive:latest

# Init DB for metadata
RUN ${HIVE_HOME}/bin/schematool -dbType derby -initSchema

# Start metastore
CMD hive --service metastore --hiveconf hive.root.logger=INFO,console