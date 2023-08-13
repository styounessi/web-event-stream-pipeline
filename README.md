<h1 align="center">
Web Event Stream Processing Pipeline 
</h1>

An end-to-end, web event stream processing pipeline that spans event generation all the way up to visualization.

![Flow](https://i.imgur.com/biteH8p.png)

## The Idea 🤔
The idea behind this repo is to stand up a basic/viable functioning environment for a stream processing pipeline centered around capturing, processing, and persistently storing web events as they occur in real-time. The layers and steps can be generally described in this manner:

1. **Event Generation:** Web events are generated, using a fake random event generator, and sent to a Kafka broker via a Kafka topic designated for 'raw' events.
2. **Broker**: The Kafka broker serves as a central hub, facilitating the reception and distribution of events through Kafka topics.
3. **Stream Processor**: The Faust stream processor takes the incoming 'raw' web events from the Kafka broker, enriches them with additional categorization, and then sends the altered data to another Kafka topic designated for 'enriched' events.
4. **Collection Engine**: The enriched web events are then consumed and indexed by Logstash via the 'enriched' Kafka topic.
5. **Data Sink**: Elasticsearch functions as the data sink and persistent storage solution for the processed data.
6. **Analysis & Visualization**: Kibana enables users to explore and analyze the stored data in Elasticsearch.

⚠️ This is purely a PoC (Proof of Concept) level project done for fun/interest. 

## Why Do This? 🤷‍♂️

### Reactive Alerting 🚨

KKibana offers powerful [alerting](https://www.elastic.co/guide/en/kibana/current/alerting-getting-started.html) and [anamoly detection](https://www.elastic.co/guide/en/kibana/current/xpack-ml-anomalies.html) features. It also integrates with tools like [PagerDuty](https://www.elastic.co/guide/en/kibana/current/pagerduty-action-type.html) to monitor and promptly address potential issues that might otherwise go unnoticed until end users report them. Quick reaction times can make a significant difference when every second counts.

### Analysis 🔍

Kibana provides extensive [dashboarding and visualization](https://www.elastic.co/guide/en/kibana/current/dashboard.html) tools for data analysis. You can aggregate events to visualize changes over time and gain valuable insights by profiling user behaviors. This level of data collection enables the making of informed decisions and to optimize experiences based on what the data shows rather than operating on ambiguity.

## Tools & Technologies 🛠️

### Web Event Generator

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

