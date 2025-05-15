
- [[Why is Kafka fast?]]
- [[Notes/Pages/Systems/Systems Design/Practical Systems/Notion/Kafka as a storage system]]
- [[Webhooks vs Kafka]]
Kafka is a stream processing system used for messaging, website activity tracking, metrics collection and monitoring, logging, event sourcing, commit logs, and real-time analytics. It’s a good fit for large scale message processing applications since it is more robust, reliable, and fault-tolerant compared to traditional message queues.

Broadly, Kafka accepts streams of **events** written by data **producers**.  Kafka stores records chronologically in **partitions** across **brokers** (servers); multiple brokers comprise a **cluster**.  Each record contains information about an event and consists of a key-value pair; timestamp and header are optional additional information.  Kafka groups records into **topics**; data **consumers** get their data by subscribing to the topics they want.



Let’s examine each of these core concepts in more detail.

#### Events

An **event** is a message with data describing the event.  For example, when a new user registers with a website, the system creates a registration event, which may include the user’s name, email, password, location, and so on.

#### Consumers and Producers

A **producer** is anything that creates data.  Producers constantly write events to Kafka. Examples of producers include web servers, other discrete applications (or application components), IoT devices, monitoring agents, and so on.  For instance:

- The website component responsible for user registrations produces a “new user is registered” event.
- A weather sensor (IoT device) produces hourly “weather” events with information about temperature, humidity, wind speed, and so on.

**Consumers** are entities that use data written by producers.  Sometimes an entity can be both a producer and a consumer; it depends on system architecture.  For example, a data warehouse could _consume_ data from Kafka, then process it and _produce_ a prepared subset for rerouting via Kafka to an ML or AI application.  Databases, data lakes, and data analytics applications generally act as data consumers, storing or analyzing the data they receive from Kafka.

LinkedIn needed to rebuild its user activity tracking pipeline as a set of real-time publish-subscribe feeds.  Activity tracking is often very high volume, as each user page view generates many activity messages (events):

- user clicks
- registrations
- likes
- time spent on certain pages
- orders
- environmental changes
- and so on

These events can be published (produced) to dedicated Kafka topics.  Each feed is available for (consumed by) any number of use cases, such as [loading into a data lake](https://www.upsolver.com/blog/blog-apache-kafka-and-data-lake) or warehouse for offline processing and reporting.

Other applications subscribe to topics, receive the data, and process it as needed (monitoring, analysis, reports, newsfeeds, personalization, and so on).

**Example scenario:** An online e-commerce platform could use Kafka for tracking user activities in real-time. Each user activity, such as product views, cart additions, purchases, reviews, search queries, and so on, could be published as an event to specific Kafka topics. These events can then be written to storage or consumed by in real-time by various microservices for recommendations, personalized offers, reporting, and fraud detection.

### **Real-time data processing**

Many systems require data to be processed as soon as it becomes available.  Kafka transmits data from producers to consumers with [very low latency](https://developer.confluent.io/learn/kafka-performance/) (5 milliseconds, for instance). This is useful for:

- Financial organizations, to gather and process payments and financial transactions in real-time, block fraudulent transactions the instant they’re detected, or update dashboards with up-to-the-second market prices. 
- Predictive maintenance (IoT), in which models constantly analyze streams of metrics from equipment in the field and trigger alarms immediately after detecting deviations that could indicate imminent failure.
- Autonomous mobile devices, which require [real-time data processing](https://www.upsolver.com/blog/build-real-time-streaming-etl-pipeline) to navigate a physical environment.
- Logistical and supply chain businesses, to monitor and update tracking applications, for example to keep constant tabs on cargo vessels for real-time cargo delivery estimates.

**Example scenario:** A bank could use Kafka for processing transactions in real-time. Every transaction initiated by a customer could be published as an event to a Kafka topic. Then, an application could consume these events, validate and process the transactions, block any suspicious transactions, and update customer balances in real-time.

### Messaging

Kafka works well as a replacement for traditional message brokers; Kafka has better throughput, built-in partitioning, replication, and fault-tolerance, as well as better scaling attributes.

**Example scenario**: A microservices-based ride-hailing app could use Kafka for sending messages between different services. For example, when a rider books a ride, the ride-booking service could send a message to the driver-matching service through Kafka. The driver-matching service could then find a nearby driver and send a message back, all in near-real time.

### Operational Metrics/KPIs

Kafka is often used for operational monitoring data. This involves aggregating statistics from distributed applications to produce centralized feeds of operational data.

**Example scenario:** A cloud service provider could use Kafka to aggregate and monitor operational metrics from various services in real-time. For example, metrics such as CPU utilization, memory usage, request counts, error rates, etc. from hundreds of servers could be published to Kafka. These metrics could then be consumed by monitoring applications for real-time visualization, alerting, and anomaly detection.

### Log Aggregation

Many organizations use Kafka to aggregate logs.  Log aggregation typically involves collecting physical log files off servers and placing them in a central repository (such as a file server or data lake) for processing. Kafka filters out the file details and abstracts the data as a stream of messages. This enables lower-latency processing and easier support for multiple data sources and distributed data consumption. Compared with log-centric systems like Scribe or Flume, Kafka offers equally good performance, stronger durability guarantees due to replication, and much lower end-to-end latency.

**Example scenario:** An enterprise with a large distributed system could use Kafka for log aggregation. Logs from hundreds or thousands of servers, applications, and services could be published to Kafka. These logs could then be consumed by a log analysis tool or a security information and event management (SIEM) system for troubleshooting, security monitoring, and compliance reporting.

You may also wish to [consult the Kafka project use case page](https://kafka.apache.org/powered-by) on the Apache Software Foundation website for more on specific deployments.

## **When Not To Use Kafka**

Given Kafka’s scope and scale it’s easy to see why you might consider it something of a Swiss army knife of big data applications.  But it’s bound by certain limitations, including its overall complexity, and there are scenarios for which it’s not appropriate.

### “Little” Data

As Kafka is designed to handle high volumes of data, it’s overkill if you need to process only a small amount of messages per day (up to several thousand).  Use traditional message queues such as RabbitMQ for relatively smaller data sets or as a dedicated task queue.

### Streaming ETL

Despite the fact that Kafka has a stream API, it’s painful to perform data transformations on the fly.  It requires that you build a complex pipeline of interactions between producers and consumers and then maintain the entire system. This requires substantial work and effort and adds complexity.  It’s best to avoid using Kafka as the processing engine for ETL jobs, especially where real-time processing is needed.  That said, there are third-party tools you can use that work with Kafka to give you additional robust capabilities – for example, to optimize tables for real-time analytics.