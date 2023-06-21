FROM apache/airflow:2.3.0-python3.9

# Change to root user
USER root

# Install Java (Java 8 not available in OS version)
RUN apt update && apt-get install -y openjdk-11-jdk && apt-get install -y ant && apt-get install -y git && apt-get clean

# Set JAVA_HOME
ARG TARGETARCH
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-${TARGETARCH}

# Change to airflow user
USER airflow

# Install requirements
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt