import os
import json
from kafka import KafkaProducer
from fake_web_events import Simulation


# Grab Kafka broker and output topic environment variables
BROKER = os.getenv('KAFKA_BROKER')
RAW_WEB_EVENTS = os.getenv('OUTPUT_TOPIC')


# Initialize a Kafka producer and configure JSON value serializer
producer = KafkaProducer(bootstrap_servers=BROKER,
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))


def event_simulator(producer, output_topic):
    '''
    Simulate web events and send them to a Kafka topic.
    '''
    web_event_sims = Simulation(user_pool_size=50, sessions_per_day=500)
    for event in web_event_sims.run(duration_seconds=999):
        producer.send(output_topic, value=event)
        print(event) # Print the simulated events for debugging purposes


if __name__ == '__main__':
    event_simulator(producer, RAW_WEB_EVENTS)
