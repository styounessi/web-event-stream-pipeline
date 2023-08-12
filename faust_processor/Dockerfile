# Using a lightweight Python base image
FROM python:3.11.4-slim-buster

# Set the working directory for the Faust processor application
WORKDIR /faust_processor

# Copy all application files to the working directory
COPY . /faust_processor

# Update apt package manager, install netcat, upgrade pip, and install dependencies in requirements.txt
RUN apt-get update && apt-get install -y netcat \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Use custom script to wait for Kafka broker availability
ENTRYPOINT ["./wait_for_broker.sh"]

# Start the Faust processor application
CMD ["./run.sh"]
