import os
import faust


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


# Class to enrich and/or manipulate web events
class EventEnrichment:
    @staticmethod
    def categorize_utm_source(utm_source):
        '''
        Categorizes UTM (Urchin Tracking Modules) sources
        into higher level groupings.

        Args:
            utm_source (str): UTM source value.

        Returns:
            str: Assigned category of the UTM source.
        '''
        if utm_source in ['google', 'bing']:
            return 'search_engine'
        elif utm_source in ['facebook', 'instagram']:
            return 'social_media'
        elif utm_source in ['mailchimp']:
            return 'email_marketing'
        else:
            return 'other/unknown'


# Faust agent to categorize UTM sources and send events to the output topic
@app.agent(input_topic)
async def categorize_utm_source_agent(events):
    async for event in events:
        utm_source = event.get('utm_source')
        if utm_source:
            source_category = EventEnrichment.categorize_utm_source(utm_source)
            event['source_category'] = source_category
        await output_topic.send(value=event)


if __name__ == '__main__':
    app.main()
