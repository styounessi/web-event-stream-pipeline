import os
import faust

from event_utils import EventEnrichment


# Grab Kafka broker and input/output topic environment variables
BROKER = os.getenv('KAFKA_BROKER')
RAW_WEB_EVENTS = os.getenv('INPUT_TOPIC')
ENRICHED_WEB_EVENTS = os.getenv('OUTPUT_TOPIC')


# Initialize Faust application
app = faust.App(
    'web_event_processor',
    broker=os.getenv('KAFKA_BROKER'),
    value_serializer='json')


# Use the Faust app to initialize input/output topics
input_topic = app.topic(RAW_WEB_EVENTS)
output_topic = app.topic(ENRICHED_WEB_EVENTS)


# Faust agent to categorize UTM sources, extract user email domains, and
# send enriched events to output topic
@app.agent(input_topic)
async def enrichment_agent(events):
    async for event in events:
        utm_source = event.get('utm_source')
        if utm_source:
            source_category = EventEnrichment.categorize_utm_source(utm_source)
            event['source_category'] = source_category
        
        user_custom_id = event.get('user_custom_id')
        if user_custom_id:
            email_domain = EventEnrichment.extract_email_domain(user_custom_id)
            event['user_email_domain'] = email_domain
        
        await output_topic.send(value=event)


if __name__ == '__main__':
    app.main()
