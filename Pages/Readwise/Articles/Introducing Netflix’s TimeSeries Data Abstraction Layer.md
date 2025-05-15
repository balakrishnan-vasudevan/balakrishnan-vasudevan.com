# Introducing Netflix’s TimeSeries Data Abstraction Layer

![rw-book-cover](https://readwise-assets.s3.amazonaws.com/static/images/article0.00998d930354.png)

## Metadata
- Author: [[Netflix Technology Blog]]
- Full Title: Introducing Netflix’s TimeSeries Data Abstraction Layer
- Category: #articles
- URL: https://medium.com/p/31552f6326f8

## Highlights
- temporal data
- the ability to ingest and store vast amounts of temporal data — often reaching petabytes — with millisecond access latency has become increasingly vital.
- TimeSeries Abstraction — a versatile and scalable solution designed to efficiently store and query large volumes of temporal event data with low millisecond latencies
- Contrary to what the name may suggest, this system is not built as a general-purpose time series database. We do not use it for metrics, histograms, timers, or any such near-real time analytics use case. Those use cases are well served by the Netflix Atlas telemetry system. Instead, we focus on addressing the challenge of storing and accessing extremely high-throughput, immutable temporal event data in a low-latency and cost-efficient manner.
- temporal data is continuously generated and utilized, whether from user interactions like video-play events, asset impressions, or complex micro-service network activities.
- High Throughput: Managing up to 10 million writes per second while maintaining high availability.
- Efficient Querying in Large Datasets: Storing petabytes of data while ensuring primary key reads return results within low double-digit milliseconds, and supporting searches and aggregations across multiple secondary attributes.
- Global Reads and Writes: Facilitating read and write operations from anywhere in the world with adjustable consistency models.
- Tunable Configuration: Offering the ability to partition datasets in either a single-tenant or multi-tenant datastore, with options to adjust various dataset aspects such as retention and consistency.
- Handling Bursty Traffic: Managing significant traffic spikes during high-demand events, such as new content launches or regional failovers.
- Cost Efficiency: Reducing the cost per byte and per operation to optimize long-term retention while minimizing infrastructure expenses, which can amount to millions of dollars for Netflix.
- Partitioned Data: Data is partitioned using a unique temporal partitioning strategy combined with an event bucketing approach to efficiently manage bursty workloads and streamline queries.
- Flexible Storage: The service is designed to integrate with various storage backends, including Apache Cassandra and Elasticsearch, allowing Netflix to customize storage solutions based on specific use case requirements.
- Scalability: The architecture supports both horizontal and vertical scaling, enabling the system to handle increasing throughput and data volumes as Netflix expands its user base and services.
- Sharded Infrastructure: Leveraging the Data Gateway Platform, we can deploy single-tenant and/or multi-tenant infrastructure with the necessary access and traffic isolation.
