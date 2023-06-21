FROM hadoop:latest

# Copy shell script that contains init script
COPY init.sh ./init.sh

# Set permissions
RUN chmod +x init.sh

# Run Script
CMD ./init.sh
