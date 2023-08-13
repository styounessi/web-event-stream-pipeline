<h1 align="center">
Web Event Stream Processing Pipeline 
</h1>

An end-to-end, web event stream processing pipeline that spans event generation all the way up to visualization.

![Flow](https://i.imgur.com/biteH8p.png)

## 🤔 The Idea
The idea behind this repo is to stand up a basic/viable functioning environment for a stream processing pipeline centered around capturing, processing, and persistently storing web events as they occur in real-time. The layers and steps can be generally described in this manner:

1. **Event Generation:** Web events are generated, using a fake random event generator, and sent to a Kafka broker via a Kafka topic designated for 'raw' events.
2. **Broker**: The Kafka broker serves as a central hub, facilitating the reception and distribution of events through Kafka topics.
3. **Stream Processor**: The Faust stream processor takes the incoming 'raw' web events from the Kafka broker, enriches them with additional categorization, and then sends the altered data to another Kafka topic designated for 'enriched' events.
4. **Collection Engine**: The enriched web events are then consumed and indexed by Logstash via the 'enriched' Kafka topic.
5. **Data Sink**: Elasticsearch functions as the data sink and persistent storage solution for the processed data.
6. **Analysis & Visualization**: Kibana enables users to explore and analyze the stored data in Elasticsearch.
