FROM ubuntu:latest

# Switch to root user
USER root

# Setting env vars
# Define a directory where the installation will be located
ENV BASE_DIR /opt

# Set different versions
ENV JAVA_VERSION 8
ENV PYTHON_VERSION 3.9


# Set Java Home env var (Vigilar con arm / amd)
ARG TARGETARCH
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-${TARGETARCH}

# Install necessary packages
RUN echo "Installing packages..." && \
    apt-get update && \ 
    apt-get install -y --no-install-recommends \
    openjdk-8-jre \
    curl \
    python3.9 \
    python3-pip \
    nano && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Update PATH 
ENV PATH ${PATH}:${JAVA_HOME}/bin

# Change to /opt directory
WORKDIR ${BASE_DIR}

# Entrypoint set up
COPY config.py ./config.py
COPY entrypoint.sh ./entrypoint.sh
RUN chmod a+x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]