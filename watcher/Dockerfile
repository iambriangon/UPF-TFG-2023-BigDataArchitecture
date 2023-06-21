FROM hadoop:latest

USER root

# Create directories
RUN mkdir -p ${BASE_DIR}/watcher/files
RUN mkdir -p ${BASE_DIR}/watcher/upload

# Copy files
COPY ./Watcher.py ./watcher
COPY ./pipeline.py ./watcher
COPY ./upload/* ./watcher/upload
COPY requirements.txt .

# Install libraries
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Init watcher
CMD python3 ./watcher/pipeline.py