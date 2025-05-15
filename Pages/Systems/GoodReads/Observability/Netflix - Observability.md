

Tags: observability, scale
Category: Articles
Company: Netflix
Status: Reading
URL: https://netflixtechblog.com/lessons-from-building-observability-tools-at-netflix-7cfafed6ab17

- At some point in business growth, we learned that storing raw application logs won’t scale. To address scalability, we switched to streaming logs, filtering them on selected criteria, transforming them in memory, and persisting them as needed.
- As applications migrated to having a microservices architecture, we needed a way to gain insight into the complex decisions that microservices were making. Distributed request tracing is a start, but is not sufficient to fully understand application behavior and reason about issues. Augmenting the request trace with application context and intelligent conclusions is also necessary.
- Besides analysis of logging and request traces, observability also includes analysis of metrics. By exploring metrics anomaly detection and metrics correlation, we’ve learned how to define actionable alerting beyond just threshold alerting.
- Our observability tools need to access various persisted data types. Choosing which kind of database to store a given data type depends on how each particular data type is written and retrieved.
- Data presentation requirements vary widely between teams and users. It is critical to understand your users and deliver views tailored to a user’s profile.

storing device and server logs didn’t scale because the increasing volume of log data caused our storage cost to balloon and query times to increase. Besides reducing our storage retention time period, we addressed scalability by implementing a real-time stream processing platform called [Mantis](https://medium.com/netflix-techblog/stream-processing-with-mantis-78af913f51a6). Instead of saving all logs to persistent storage, Mantis enables our users to stream logs into memory, and keep only those logs that match SQL-like query criteria. Users also have the choice to transform and save matching logs to persistent storage.

The key takeaway is that storing all logs in persistent storage won’t scale in terms of cost and acceptable query response time. An architecture that leverages real-time event streams and provides the ability to quickly and iteratively identify the relevant subset of logs is one way to address this problem.

Since most inter-process communication uses HTTP and [gRPC](https://grpc.io/docs/guides/) (with the trend for newer services to use gRPC to benefit from its binary protocol), we implemented request interceptors for HTTP and gRPC calls. These interceptors publish trace data to Apache Kafka, and a consuming process writes trace data to persistent storage.

![image.png](image%208.png)

The smaller squares beneath a server indicate individual operations. Gray-colored servers don’t have tracing enabled.

A distributed request trace provides only basic utility in terms of showing a call graph and basic latency information. What is unique in our approach is that we allow applications to add additional identifiers to trace data so that multiple traces can be grouped together across services. For example, for playback request traces, all the requests relevant to a given playback session are grouped together by using a playback session identifier. We also implemented additional logic modules called ***analyzers*** to answer common troubleshooting questions. Continuing with the above example, questions about a playback session might be why a given session did or did not receive 4K video, or why video was or wasn’t offered with High Dynamic Range.

# **Analysis of Metrics**

Besides analysis of logging and request traces, observability also involves analysis of metrics. Because having users examine many logs is overwhelming, we extended our offering by publishing log error counts to our metrics monitoring system called [Atlas](https://medium.com/netflix-techblog/introducing-atlas-netflixs-primary-telemetry-platform-bd31f4d8ed9a), which enables our users to quickly see macro-level error trends using multiple dimensions, such as device type and customer geographical location. An alerting system also allows users to receive alerts if a given metric exceeds a defined threshold. In addition, when using Mantis, a user can define metrics derived from matching logs and publish them to Atlas.

Next, we have implemented statistical algorithms to detect anomalies in metrics trends, by comparing the current trend with a baseline trend.

# **Data Persistence**

We store data used by our tools in Cassandra, Elasticsearch, and Hive. We chose a specific database based primarily on how our users want to retrieve a given data type, and the write rate. For observability data that is always retrieved by primary key and a time range, we use Cassandra. When data needs to be queried by one or more fields, we use Elasticsearch since multiple fields within a given record can be easily indexed. Finally, we observed that recent data, such as up to the last week, is accessed more frequently than older data, since most of our users troubleshoot recent issues. To serve the use case where someone wants to access older data, we also persist the same logs in Hive but for a longer time period.

[Cassandra](https://docs.datastax.com/en/cassandra/3.0/cassandra/dml/dmlIntro.html) provides the best, highest per-record write and read rates, but is restrictive for reads because you must decide what to use for a row key (a unique identifier for a given record) and within each row, what to use for a column key, such as a timestamp. In contrast, Elasticsearch and Hive provide more flexibility with reads because Elasticsearch allows you to index any field within a record, and Hive’s SQL-like query language allows you to match against any field within a record. However, since Elasticsearch is primarily optimized for free text search, its indexing overhead during writes will demand more computing nodes as write rate increases. For example, for one of our observability data sets, we initially stored data in Elasticsearch to be able to easily index more than one field per record, but as the write rate increased, indexing time became long enough that either the data wasn’t available when users queried for it, or it took too long for data to be returned. As a result, we migrated to Cassandra, which had shorter write ingestion time and shorter data retrieval time, but we defined data retrieval for the three unique keys that serve our current data retrieval use cases.

For Hive, since records are stored in files, reads are relatively much slower than Cassandra and Elasticsearch because Hive must scan files. Regarding storage and computing cost, Hive is the cheapest because multiple records can be kept in a single file, and data isn’t replicated. Elasticsearch is most likely the next more expensive option, depending on the write ingestion rate. Elasticsearch can also be configured to have [replica shards](https://www.elastic.co/guide/en/elasticsearch/guide/current/replica-shards.html) to enable higher read throughput. Cassandra is most likely the most expensive, since it encourages replicating each record to [more than one replica](https://docs.datastax.com/en/cassandra/3.0/cassandra/architecture/archDataDistributeReplication.html?hl=data%2Creplication) in order to ensure reliability and fault tolerance.

Some of those new feature requests involve displaying data in a view customized for specific user groups, such as device developers, server developers, and Customer Service. ‘’

Examining a given log type may require domain expertise that not all users may have. For example, for a given log from a Netflix device, understanding the data in the log requires knowledge of some identifiers, error codes, and some string keys. Our tools try to minimize the specialized knowledge required to effectively diagnose problems by joining identifiers with the data they refer to, and providing descriptions of error codes and string keys.