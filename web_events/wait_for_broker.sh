#!/bin/sh

echo "Waiting for Kafka broker to be available..."

while ! nc -z kafka 29092; do
  sleep 1
done

echo "Kafka broker available. Starting services..."

exec "$@"
