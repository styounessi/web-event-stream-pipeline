<h1 align="center">
Web Event Stream Processing Pipeline 
</h1>

An end-to-end web event stream processing pipeline encompassing event generation through visualization.

![Flow](https://i.imgur.com/biteH8p.png)

## The Idea 🤔
The idea behind this repo is to stand up a basic/viable functioning environment for a stream processing pipeline centered around capturing, processing, and persistently storing web events as they occur in real-time. The layers and steps can be generally described in this manner:

1. **Event Generation:** Web events are generated, using a fake random event generator, and sent to a Kafka broker via a Kafka topic designated for 'raw' events.
2. **Broker**: The Kafka broker serves as a central hub, facilitating the reception and distribution of events through Kafka topics.
3. **Stream Processor**: The Faust stream processor takes the incoming 'raw' web events from the Kafka broker, enriches them with additional categorization, and then sends the altered data to another Kafka topic designated for 'enriched' events.
4. **Collection Engine**: The enriched web events are then consumed and indexed by Logstash via the 'enriched' Kafka topic.
5. **Data Sink**: Elasticsearch functions as the data sink and persistent storage solution for the processed data.
6. **Analysis & Visualization**: Kibana enables users to explore and analyze the stored data in Elasticsearch.

⚠️ This project is done for fun/interest and to experiment with different ways to process, massage, and enrich events. 

## Why Do This? 🤷‍♂️

### Reactive Alerting 🚨

Kibana offers [alerting](https://www.elastic.co/guide/en/kibana/current/alerting-getting-started.html) and [anomaly detection](https://www.elastic.co/guide/en/kibana/current/xpack-ml-anomalies.html) features. It also integrates with tools like [PagerDuty](https://www.elastic.co/guide/en/kibana/current/pagerduty-action-type.html) to monitor and promptly address potential issues that might otherwise go unnoticed until end users report them.

### Analysis 🔍

Kibana provides extensive [dashboarding and visualization](https://www.elastic.co/guide/en/kibana/current/dashboard.html) tools for data analysis. You can aggregate events to visualize changes over time and gain valuable insights by profiling user behaviors. This level of data collection enables the making of informed decisions and to optimize experiences based on what the data shows rather than operating on ambiguity.

Basically, the goal is to limit being caught off guard by flying blind. As well as being able to examine events in near real-time rather than after the fact. 

## Tools & Technologies 🛠️

### Web Event Generator 🌐

Events are generated using the very handy [Fake Web Events](https://github.com/andresionek91/fake-web-events) library. A typical fake event looks like this:

```json
{
  "event_timestamp": "2020-07-05 14:32:45.407110",
  "event_type": "pageview",
  "page_url": "http://www.dummywebsite.com/home",
  "page_url_path": "/home",
  "referer_url": "www.instagram.com",
  "referer_url_scheme": "http",
  "referer_url_port": "80",
  "referer_medium": "internal",
  "utm_medium": "organic",
  "utm_source": "instagram",
  "utm_content": "ad_2",
  "utm_campaign": "campaign_2",
  "click_id": "b6b1a8ad-88ca-4fc7-b269-6c9efbbdad55",
  "geo_latitude": "41.75338",
  "geo_longitude": "-86.11084",
  "geo_country": "US",
  "geo_timezone": "America/Indiana/Indianapolis",
  "geo_region_name": "Granger",
  "ip_address": "209.139.207.244",
  "browser_name": "Firefox",
  "browser_user_agent": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_5; rv:1.9.6.20) Gecko/2012-06-06 09:24:19 Firefox/3.6.20",
  "browser_language": "tn_ZA",
  "os": "Android 2.0.1",
  "os_name": "Android",
  "os_timezone": "America/Indiana/Indianapolis",
  "device_type": "Mobile",
  "device_is_mobile": true,
  "user_custom_id": "vsnyder@hotmail.com",
  "user_domain_id": "3d648067-9088-4d7e-ad32-45d009e8246a"
}
```

The volume of events can be adjusted up or down based on testing needs. A look inside the Docker container for this application shows the stream of events as they generate.

![Events](https://i.imgur.com/zqtqxm6.gif)

In real-life scenarios, dealing with the sheer avalanche of events being logged can quickly turn into a major challenge.

### Apache Kafka 📡

> Apache Kafka is a distributed event store and stream-processing platform. It is an open-source system developed by the Apache Software Foundation written in Java and Scala. The project aims to provide a unified, high-throughput, low-latency platform for handling real-time data feeds.

The broker is like a mail room. It takes in all the mail and makes sure they get to the right recipients. It doesn't care what's inside the notes; it just makes sure they get where they need to go.

The `raw-web-events` topic receives events as they are generated, while the `enriched-web-events` topic (more on this in the Faust section) collects the processed events that are prepared for persistent storage.

### Faust ⚙️

>Faust is a Python library designed for building and deploying high-performance, event-driven, and streaming applications. It is particularly well-suited for processing and analyzing  >continuous streams of data, making it a powerful tool for real-time data processing, event-driven architectures, and stream processing pipelines.

⚠️ The original Faust library was essentially abandoned by Robinhood, there is an actively maintained community fork of Faust called `faust-streaming` that is used for this project. You can read about it here: [LINK](https://faust-streaming.github.io/faust/)

Faust is used in this pipeline to receive raw web events, categorize the UTM source of each event into higher level groupings using the `categorize_utm_source` method of the `EventEnrichment` class, and to send the events to the `enriched-web-events` topic. The new field will look like this example:

```json
"source_category": "social_media"
```

Another basic manipulation would be to remove certain fields that are not worth keeping while retaining the fields that are valuable to end users. 

### ELK Stack 📚

>The ELK Stack is a widely used combination of three tools: Elasticsearch, Logstash, and Kibana. It's designed to help organizations collect, process, store, and analyze
>large volumes of data, especially log and event data, for various purposes such as monitoring, troubleshooting, and business insights.

#### Logstash 🌉

The `logstash.conf` file included in this repo configures the Logstash service needed to ingest data from a Kafka topic, parse and convert the JSON content into individual fields, and then forward the processed data to Elasticsearch for storage and indexing. The configuration allows for dynamic date-based indexing:

`index => "${ELASTIC_INDEX}-%{+YYYY.MM.dd}`

The snippet above creates an index name that includes both a customizable prefix and a datestamp. This allows for time-based data segmentation, where each day's data is stored in a separate index.

#### Elasticsearch 🗄️

Elasticsearch serves as the persistent data sink layer that stores and makes data searchable and analyzable. It's capable of handling large volumes of structured and unstructured data.

#### Kibana 📊

In conjunction with Elasticsearch, Kibana is the data visualization and exploration tool that can be used to interact with the event data stored in Elasticsearch.

![Hits](https://i.imgur.com/dsmiflj.gif)

You can see the new events with each refresh and all dashboards, configured aggregations, etc are all updated with the changing data.

<img src="https://i.imgur.com/kPgrzLQ.png" width="500"/> <img src="https://i.imgur.com/PgZjWYy.png" width="500"/>

### Docker 🐳 & Docker Compose 🐙

This project is fully dockerized and includes a `docker-compose.yml` file that orchestrates the multi-container setup. Each service is configured with dependencies to ensure a proper startup sequence and consistent runtime.

All containers are spun up using `docker-compose up` with `-d` added at the end if you prefer detached mode.

The `zookeeper` service exists to support Kafka and is spun up with two volumes: `zk-data:/var/lib/zookeeper/data` & `zk-logs:/var/lib/zookeeper/log`. The health check periodically attempts to establish a network connection to the `zookeeper` service on port `2181` using the `nc` command. If the connection is successful, the service is considered healthy.

> **Note:** Apache Kafka is moving away from Zookeeper in the near future, but it remains viable for now. You can read more about this below:
>
> Apache Kafka Raft (KRaft) is the consensus protocol introduced in KIP-500 to remove Apache Kafka’s dependency on ZooKeeper for metadata management. This significantly simplifies Kafka’s architecture by consolidating metadata responsibility within Kafka itself, eliminating the split between two systems.

The `kafka` container initializes as a Kafka broker; it depends on the `zookeeper` service to become healthy before starting, ensuring proper coordination. It also employs the same `nc` health check as the `zookeeper` container. The volume `kafka-data:/var/lib/kafka/data` is defined to ensure data durability and seamless recovery in case of container restarts.

Meanwhile, `kafka-topics-init` waits for both the `kafka` and `zookeeper` services to become healthy before proceeding. It executes the shell script defined in the `entrypoint` command to create the required topics for this pipeline. Once this task is completed, it shuts down.

The `web-events` and `faust-processor` containers are built from their respective Dockerfiles, which define the build criteria and execution scripts. Both containers verify the readiness of the Kafka broker before proceeding; they rely on the broker being operational for successful execution.

The `setup` service/container configures an 'Elastic' instance with security features. It ensures the setup of user authentication, SSL encryption, and certificates. This is necessary even in development settings, as Elastic Versions 8.0 and higher enable security by default. Once implemented, the setup service shuts down. All ELK stack services depend on the successful health condition of the `setup` container.

All ELK stack services have designated volumes to preserve configurations and settings across containers.

The `logstash-01` service depends on the included `logstash.conf` file to define the input, filter, and output conditions related to interfacing with Kafka and Elasticsearch for data bridging.

The `es-01` service initializes a primary Elasticsearch node within the ELK stack. It acts as a primary data repository, indexing and storing enriched events from Kafka via the `logstash-01` service, enabling querying and analysis through Kibana.

The `kibana` service offers a web-based interface for visualizing and interacting with data stored in Elasticsearch. It relies on the readiness of both the `es-01` and `setup` services to ensure a secure and operational environment. A designated volume, `kibanadata:/usr/share/kibana/data`, is employed to persistently store user settings, dashboards, and configurations across container restarts.

### Environment Varible File 🔑

Not included in this report is an `.env` file that will need to go in the root project directory. It will contain sensitive and not-so-sensitive variables for the ELK stack setup and configuration. You can see the entire structure of the file in the template below:

```env
# Password for the 'elastic' user (at least 6 characters)
ELASTIC_PASSWORD=your-password-here

# Password for the 'kibana_system' user (at least 6 characters)
KIBANA_PASSWORD=your-password-here

# Version of the Elastic Stack
STACK_VERSION=use-desired-version-here

# Set the cluster name
CLUSTER_NAME=your-cluster-name

# Set to 'basic'
LICENSE=basic

# Port to expose Elasticsearch HTTP API to the host
ES_PORT=9200

# Port to expose Kibana to the host
KIBANA_PORT=5601

# Increase or decrease based on the available host memory (in bytes)
ES_MEM_LIMIT=1073741824
KB_MEM_LIMIT=1073741824
LS_MEM_LIMIT=1073741824
```
