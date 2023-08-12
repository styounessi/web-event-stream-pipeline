# Using a lightweight Python base image
FROM python:3.11.4-slim-buster

# Set the working directory for the web_events application
WORKDIR /web_events

# Copy all application files to the working directory
COPY . /web_events

# Update apt package manager, install netcat, upgrade pip, and install dependencies in requirements.txt
RUN apt-get update && apt-get install -y netcat \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Use custom script to wait for Kafka broker availability
ENTRYPOINT ["./wait_for_broker.sh"]

# Run the web event generator application
CMD ["python", "web_event_generator.py"]
