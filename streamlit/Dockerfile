FROM python:3.9-slim-buster

WORKDIR /app

# Get some packages
RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-11-jdk \
    curl \
    nano \
    software-properties-common \
    libsasl2-dev \
    libsasl2-2 \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME for PySpark
ARG TARGETARCH
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-${TARGETARCH}

# Copy files
COPY visualization.py .
COPY requirements.txt .

# Install libraries
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Run (cmd for reference)
# CMD ["streamlit", "run", "visualization.py", "--server.port=8501", "--server.address=0.0.0.0"]