# Categorizing How Distributed Databases Utilize Consensus Algorithms

![rw-book-cover](https://readwise-assets.s3.amazonaws.com/static/images/article0.00998d930354.png)

## Metadata
- Author: [[Adam Prout]]
- Full Title: Categorizing How Distributed Databases Utilize Consensus Algorithms
- Category: #articles
- URL: https://medium.com/p/492c8ff9e916

## Highlights
- Consensus for Metadata” (CfM) and “Consensus for Data” (CfD). As their names suggest, both designs use a consensus algorithm (Raft, Paxos, etc.) to handle failures and store data, but they differ in the type of data that is managed by consensus.
- Consensus for Metadata (CfM)
- This design is used by systems such as Apache Kafka, FoundationDB and SingleStoreDB/MemSQL among others. CfM stores high level metadata about the state of the cluster (i.e., which hosts are online vs offline, which shards are stored on which hosts, etc.) in a centralized set of coordinator nodes (in green on the diagram). The coordinator nodes themselves don’t typically store any of the user’s data (i.e., they don’t store shards), just metadata. The coordinators use a consensus algorithm to replicate metadata changes and keep metadata available to the cluster if coordinators node fail. The user data itself in CfM is replicated using primary — secondary replication algorithms specific to each database system (synchronous replication of a transaction log typically). These replication algorithms only worry about transmitting data, and not about what how to elect a new primary if a primary fails (the blue replication arrows in figure 1). When a data node becomes unhealthy the centralized coordinator is responsible for electing a new primary for this nodes shards from its replica’s(triggering a failover) and updating its cluster metadata appropriately. CfM separates replication of data from the algorithms used for election/failover. This involves a protocol between the data nodes and the coordinators so the coodinators know which replica’s are safe to failover to (have all committed data).
- Consensus for Data (CfD)
- It uses consensus replication to store user data and keep it available. The consensus algorithm running on the data nodes is responsible for electing a new primary for each shard if a data node dies. Google Spanner and modern MongoDB are the most popular examples of this design. CfD databases may or may not have a centralized coordinator nodes for other reasons (ie., running DDL operations like adding/removing nodes), but this coordinator won’t be responsible for acting on data node failures.
- Consensus for Data examples:
- Spanner
- MongoDB
- DynamoDB
- CosmosDB
- CockroachDB
- TiDB
- Yugabyte
- Redpanda
- Consensus for Metadata examples:
- Apache Kafka
- FoundationDB (and thus Snowflake which uses FoundationDB for metadata)
- MemSQL/SingleStore
- Clickhouse
- ElasticSearch
- Redshift
- PlanetScale
- AWS Aurora
- Azure SQL Hyperscale
- Neon (for WAL writes) (*)
- Advantages of Consensus For Metadata
