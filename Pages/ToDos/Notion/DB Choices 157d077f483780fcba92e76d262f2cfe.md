# DB Choices

Tags: databases
Category: Articles
Company: general
Status: Reading

| Read heavy | Workload | These systems prioritize fast and frequent data retrieval. Examples include:
1. Content delivery platforms (e.g., blogs, video streaming sites).
2. Search engines or dashboards with analytics. | • **Relational Databases (SQL)**: MySQL, PostgreSQL — Use efficient indexing to optimize query performance.
• **Key-Value Stores**: Redis, Memcached — Excellent for ultra-fast, in-memory data retrieval.
• **Search Databases**: Elasticsearch — Ideal for full-text search and query-heavy systems.
• **Replication Strategies**: Employ *read replicas* to distribute load and improve availability. |
| --- | --- | --- | --- |
|  | Latency |  | • Use caching layers (e.g., Redis, Memcached) to minimize latency.
• Optimize query patterns and database indexes. |
|  | CAP |  | Consistency might be critical (e.g., for analytics or financial data). Use relational databases or strongly consistent NoSQL options. |
|  | Horizontal Scaling |  | Add read replicas or shard data across multiple nodes. |
| Write heavy | Workload | These systems prioritize storing large volumes of data quickly. Examples include:
1. Event logging systems.
2. IoT platforms or real-time monitoring systems. | • **NoSQL Databases**: MongoDB, Cassandra — Designed for horizontal scaling and high write throughput.
• **Time-Series Databases**: InfluxDB, TimescaleDB — Optimized for time-stamped data, perfect for continuous writes.
• **Columnar Databases**: HBase, Bigtable — Handle analytical workloads with frequent writes.
• **Queue-Based Systems**: Kafka, RabbitMQ — Buffer writes using queues to manage throughput efficiently. |
|  | latency |  | 
• Use batch writes or asynchronous writes to handle high loads efficiently.
• Avoid heavy constraints or triggers that can slow down write operations. |
|  | CAP |  | Availability often takes precedence, especially for event logging or monitoring. Use eventually consistent databases like Cassandra or DynamoDB. |
|  | Horizontal Scaling |  | Use distributed databases like Cassandra or DynamoDB that handle partitioning seamlessly. |

| DB | Replication | Conflict Resolution | Consistency |
| --- | --- | --- | --- |
| Ficus, Coda | *replicate files for high availability at the expense*
*of consistency. Update conflicts are typically managed using*
*specialized conflict resolution procedures.* | *perform system*
*level conflict resolution* | Eventual consistency |
| Bayou | *distributed relational*
*database system that allows disconnected operations*
*and provides eventual data consistency.* | Allows application level conflict resolution | Eventual Consistency |
| Farsite | *achieves high availability and scalability using*
*replication.* |  |  |
| GFS | *simple design with a single*
*master server for hosting the entire metadata and where*
*the data is split into chunks and stored in chunk servers.*
*However the GFS master is now made fault tolerant using*
*the Chubby[3] abstraction.* |  |  |
| Dynamo | *allows read and*
*write operations to continue even during network partitions*
*and resolves update conflicts using different conflict resolution*
*mechanisms, some client driven.* | *Dynamo's Gossip*
*based membership algorithm helps every node maintain information*
*about every other node. Dynamo can be de ned*
*as a structured overlay with at most one-hop request routing.*
*Dynamo detects updated conflicts using a vector clock*
*scheme, but prefers a client side conflict resolution mechanism.*
*A write operation in Dynamo also requires a read to*
*be performed for managing the vector timestamps. This is*
*can be very limiting in environments where systems need*
*to handle a very high write throughput.* |  |
| Traditional replicated DBs | *focus on the problem of guaranteeing strong consistency of replicated data. Although strong consistency provides the application writer a convenient programming model, these systems are limited in scalability and availability [10].*  |  | *These systems are not capable of handling network partitions because they typically provide strong consistency guarantees.* |
| Bigtable | *provides*
*both structure and data distribution but relies on a distributed  file system for its durability.* |  |  |

![IMG_4433.jpeg](IMG_4433.jpeg)

| DB | Features | Why? |
| --- | --- | --- |
| Aurora | Amazon Aurora is a relational database service for OLTP workloads offered as part of Amazon Web Services (AWS) |  |
| BigTable | Bigtable is a distributed storage system for managing structured data that is designed to scale to a very large size: petabytes of data across thousands of commodity servers. Many projects at Google store data in Bigtable, including web indexing, Google Earth, and Google Finance. |  |
| Cassandra | Cassandra is a distributed storage system for managing very large amounts of structured data spread out across many commodity servers, while providing highly available service with no single point of failure. Cassandra is a distributed storage system for managing very large amounts of structured data spread out across many commodity servers, while providing highly available service with no single point of failure.  | Inbox search |
| Dynamo |  a highly available key-value storage system that some of Amazon’s core services use to provide an “always-on” experience.  To achieve this level of availability, Dynamo sacrifices consistency under certain failure scenarios. It makes extensive use of object versioning and application-assisted conflict resolution in a manner that provides a novel interface for developers to use.  |  |
| DynamoDB | Amazon DynamoDB is a NoSQL cloud database service that supports fast and predictable performance at any scale. D |  |
| Hbase | Apache HBase is an open-source column-oriented NoSQL database built on top of Hadoop Distributed File system (HDFS) and is written in Java language. It is implemented on Google’s BigTable paper. It offers distributed fault-tolerance, horizontal scalability, automatic sharding, automatic failover support, random read/write access to huge data sets, support for Java API and MapReduce jobs. The hybrid architecture enables real time querying capabilities with the speed of key-value store using HDFS and offline or batch processing using Hadoop’s MapReduce programming model. |  |
| Spanner | Spanner is Google’s scalable, multiversion, globally distributed, and synchronously replicated database. It is the first system to distribute data at global scale and support externally-consistent distributed transactions. |  |
| Monarch | Monarch is a globally-distributed in-memory time series database system in Google. |  |